# Infrastructure

Shepherd Nova comprises several distributed nodes and backend servers connected via Ethernet.
Each node includes an observer and up to two devices under test, called targets.
Typical targets are low-power IoT devices equipped with MCU, wireless transceivers, and peripherals such as sensors.
The observers implement all services in hardware and software, emulating energy-harvesting conditions and collecting time-stamped observations.
The backend servers provide harvesting data for emulation to the observers, store observations, coordinate observer operations (e.g. starting and stopping experiments), and interact with users who provide the target firmware and configuration of an experiment.

Please consult the paper for an in-depth system description.
The paper also evaluates topics like faithfulness and repeatability - the cornerstones of the testbed.

```{figure} /media/testbed_sys_overview.svg
:align: center
:alt: High-level architecture of Shepherd Nova
:width: 500

**High-level architecture of Shepherd Nova:**
Each testbed node consists of an observer and up to two targets.
The observers are connected over Ethernet with multiple backend servers
```

```{figure} /media/testbed_sys_observer.svg
:align: center
:alt: HW & SW architecture of an observer
:width: 500

Mapping of software modules to hardware components on a Shepherd Nova observer,
showing the interaction and data flow between modules.
```

```{attention}
TODO: add link to paper
```

## Building a Chain of Trust

For the design of the system we aimed for complete transparency and openness.
But how can the user be sure that the testbed functioned as expected during an experiment?
The following subsections are building on top of the topics already presented in the paper.
We will describe our extensive warning-system which offers various checks.
The goal was to supervise and self-diagnose every critical component during operation.

**If something unplanned or bad happens, you will most likely hear about it.**

Extensive logs are usually included in each result-file.
Please note, that it's not needed to comb through every entry to validate an experiment.
These logs are mainly there for debugging in case something goes wrong.
When using the provided `shepherd-data` utilities, the tool will usually report automatically if warnings and errors were emitted during the experiment.

With the additional goal of failing early, the testbed tries to verify states and configurations as soon as possible.
The user can see that during the creation of an invalid experiment, i.e. when a target is requested by two observer configurations.
That concept was applied throughout the architecture.

## Observer Logs

For executing an experiment, three software units work together in unison:

- the testbed service called `shepherd-sheep` which orchestrates all subsystems
- a `kernel module` which coordinates hardware-access, data-flows and time-sync to the PRU-coprocessors
- the firmware on the `PRUs`, running the virtual power source, gpio-tracer and accessing the analog frontend

Each of these systems can emit various warnings and errors which are recorded together with the verbose logs in the resulting hdf5-file.
Operation of the kernel module is monitored by capturing the whole kernel log (`dmesg`).
Same goes for the operation of the PRUs - which are monitored by and through the kernel module.
Each PRU can send data and error-states via a dedicated message-system to the kernel module.
Some messages / errors are only reported through the kernel log, but most errors are handed to the sheep-software and reported there.

### Supervision

Let's have a look at the individual autonomous & supervised observer-tasks:

- patching the node-ID and converting the firmware to intel-hex
- programming and validating the firmware written to each MCU on the target
- starting, running and ending an experiment

It makes no sense to list every error-case, but to pick a few:

- input files (environments) are validated upon opening them
- misbehaving synchronization between observers (PTP & PHC2SYS)
- misbehaving sync between system and PRUs (which can be a result of a flaky outer sync)
- a tracer that misses starting time or ends too early is detected
- The supervisor for the buffers can detect backpressure, under- & **overflows**, and also **harmed canaries** between separate RAM-sections
  - Note: **backpressure** can occur when the gpio-tracer samples more data (capable of 1+ MSps) than the filesystem can handle (~ 400 kSps). In that case buffer-sections need to be discarded to keep the system responsive. This will produce a timestamped error-log.

### Statistics

In addition to the discrete warnings each observer also records & timestamps utilization statistics:

- PRU0 running the virtual source monitors it's execution time. The recorder will additionally warn about broken real-time conditions. This is important as it delays the following chip-select flank for triggering the ADC isochronously.
- PRU1 running the GPIO-Tracer monitors the worst time between reading GPIO-states. Shepherd guarantees 1 MSps, but often surpasses that. In comparison to tracing power, the sampling rate varies. Just checking unchanged states currently results in 1.4 MHz minimal, 2.2 MHz mean and 2.9 MHz maximum rate. When states change and data has to be written, the rates will degrade to 1.1, 1.6 & 1.7 MHz respectively.
- Linux allows recording system utilization, specifically from CPU, RAM, network-IO & filesystem-IO
- Linux also allows recording synchronization stats from NTP, PTP and PHC2SYS

## Unittests & Quality Assurance

Most software for this testbed is directly unit-tested during development.
Tests that are hardware independent are also executed on GitHub via continuous integration workflows.
Firmwares and other hard-to-test elements are at least compiled and / or run through a static analysis in these workflows.
Drafting new releases is only possible when these workflows pass.
This won't make the system perfect, but at least catches a big chunk of possible flaws.

As an example the software-stack of the observer offers a special loopback-test to validate data-consistency for the following route used by emulation-experiments:

```
    Input-File
      ↪ pySheep
        ↪ Input-RAM-Buffer
          ↪ Kernel Module
            ↪ OCMC-Buffer
              ↪ PRU0 (Loopback)
                ↪ Output-RAM-Buffer
                  ↪ pySheep
                    ↪ Output-File
```

## Time Synchronization

For running the testbed we are less interested in an absolute time, but rather a **relative sync** between all observers.
We aim for sub 1 us accuracy and have chosen to use PTP on network level.
The PTP-server is a Raspberry PI 4 that is first in line to support **hardware timestamping** -
an essential feature that corrects timestamps right before packets are sent onto the wire.
The routing is handled by a single level 3 Cisco-switch.
It uses a dedicated FPGA instead of a CPU to reduce latency and jitter.
The switch itself supports no PTP-features like transparent clock.

```{figure} /media/sync_setup_ptp.svg
:align: center
:alt: Synchronization setup and results.
:width: 500

**Synchronization setup and results**:
two nodes are synchronized to one PTP server over a standard Ethernet switch.
```

Each observer is utilizing a BeagleBone - an SBC that is also capable of hardware timestamping.
Via PTP & PHC2SYS the Linux system time is adjusted.
Each Shepherd observer records the statistics of both services to allow later diagnostics.
In a last step the system time is synchronized to the PRU-coprocessors.
We have designed a dedicated self-tuning PI-controller that runs inside the kernel module and converges within less than 20 seconds.
The figure above shows the relative sync between two exemplary observers in the testbed.
Signals were taken from the chip-select input of the ADC as it is precisely controlled by PRU0 for isochronous timing.

```{seealso}
1) Additional information about the PI-controller and an accompanying simulation can be found in the [source-directory](https://github.com/nes-lab/shepherd/tree/main/software/kernel-module) of the kernel module.
2) Documentation about the measurement can be found [in the main repo](https://nes-lab.github.io/shepherd/dev/time_sync_analysis/readme.html).
```

## Virtual Power Source & Harvester

The main routines for the virtual power source run inside the PRU0-coprocessor.
Besides being partly covered by unittests, these routines unfortunately act largely like a black box.
To counteract the issue, we took three additional steps:

- The virtual power source, including the harvester, was fully ported to python as a 1:1 functional-copy. A simulation can be run by adding a virtual target. Internal states and behaviors can be easily debugged similar to [Simba](https://github.com/LENS-TUGraz/simba). While Simba was not designed with real-time and hardware in the loop in mind, the concepts have the same goal.
- The C-code, running inside the PRU, can be compiled to a shared library with an interface for python. Beside the python-port, this can act as an additional plugin-replacement for an emulation experiment. All three versions can be run against each other and compared.
- mathematical models, behaviors and parameters were validated during two master theses.

For more insight during the actual emulation the user can leverage the following config and data:

- the power-good-signal (battery OK) for the target is recorded together with the GPIO-Trace
- configurations with static output voltage (buck-converter) allow to record the voltage levels and output-current of the virtual storage capacitor instead

```{seealso}
More details can be found in the [section covering the virtual power source](/content/virtual_source.md).
```

## Calibration

The analog frontend of each observer is calibrated with a Keithley 2604B SMU to allow precise measurements.
Calibration data is stored on an EEPROM on the same PCB as the frontend and will be copied to the result-file during an experiment.
Additionally, the [data is stored online](https://github.com/orgua/shepherd-v2-planning/tree/main/doc_testbed/calibration_cape_24b_2023_09) to avoid loss and enable quick lookup.
During recording the raw values from the ADCs are not altered, but stored as is in the hdf5-file.
This would allow for later re-calibration and easily correcting the result-files, in case an issue is found with an individual calibration.
Calibrations made two years apart showed excellent long time stability of the frontend.
More details can be found in the paper.
