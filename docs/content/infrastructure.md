# Infrastructure

Shepherd Nova comprises several distributed nodes and backend servers connected via Ethernet.
Each node includes an observer and up to two devices under test, called targets.
Typical targets are low-power IoT devices equipped with MCU, wireless transceivers, and peripherals such as sensors.
The observers implement all services in hardware and software, emulating energy-harvesting conditions and collecting time-stamped observations.
The backend servers provide harvesting data for emulation to the observers, store observations, coordinate observer operations (e.g. starting and stopping experiments), and interact with users who provide the target firmware and configuration of an experiment.

Please consult the paper for an in-depth system description.
The paper also evaluates topics like faithfulness and repeatability - the cornerstones of the testbed.

```{attention}
TODO: add link to paper
```

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

## Building a Chain of Trust

For the design of the system we are aiming for complete transparency and openness. 
But how can the user be sure that the testbed functioned as expected during an experiment?
The following subsections are building ontop of the topics already presented in the paper.
We will describe our extensive warning-system which offers various checks.
The goal was to supervise and self-diagnose every critical component during operation.

Extensive logs are usually included in each result-file.
Please note, that it's not needed to comb through every entry to validate an experiment.
These logs are mainly there for debugging in case something goes wrong.
When using the provided `shepherd-data` utilities via the command line interface, the tool will usually warn automatically if warnings and errors were emitted during the experiment.

In addition to the warning-system the testbed tries to validate situations asap.
Failing early was an additional goal.
The user can see that during the creation of an invalid experiment, i.e. when a target is requested by two observer configurations.

## Observer Logs

For executing an experiment, three software units work together in unison:

- the testbed service called `shepherd-sheep` which orchestrates all subsystems
- a `kernel module` which coordinates hardware-access, data-flows and time-sync to the PRU-coprocessors
- the firmware on the `PRUs`, running the virtual power source, gpio-tracer and accessing the analog frontend

Each of these systems can emit various warnings and errors which are recorded together with the verbose logs in the resulting hdf5-file.
Operation of the kernel modul is monitored by capturing the whole kernel log (`dmesg`).
Same goes for the operation of the PRUs - which are monitored by the kernel module. 
Each PRU can send data and error-states via a dedicated message-system to the kernel module.
Some errors are only reported through the kernel log, but most errors are handed to the sheep-software and reported there.

### Observer Tasks

Let's have a look at the individual autonomous & supervised observer-tasks:

- patching the node-ID and converting the firmware to intel-hex
- programming and validating the firmware written to each MCU on the target
- starting, running and ending an experiment

It makes no sense to list every error-case, but to pick a few:

- input files (environments) are validated upon opening them
- misbehaving synchronization between observers (PTP & PHC2SYS)
- misbehaving sync between system and PRUs (which can be a result of a flaky outer sync)
- a tracer that misses a starting time or ends too early is detected
- The supervisor for the buffers can detect backpressure, under- & **overflows**, and also **harmed canaries** between separate RAM-sections
  - Note: **backpressure** can occur when the gpio-tracer samples more data (capable of 1+ MSps) than the filesystem can handle (~ 400 kSps). In that case buffer-sections need to be discarded to keep the system responsive. This will produce a timestamped error-log.

### Observer Statistics

In addition to the discrete warnings each observer also records & timestamps utilization statistics:

- PRU0 running the virtual source monitors it's execution time. The recorder will additionally warn about broken real-time conditions. This is important as it delays the following chip-select flank for triggering the ADC isochronously. 
- PRU1 running the GPIO-Tracer monitors the worst time between reading GPIO-states. Shepherd guarantees 1 MSps, but often surpasses that. In comparison to tracing power, the sampling rate varies. Just checking unchanged states currently results in 1.4 MHz minimal, 2.2 MHz mean and 2.9 MHz maximum rate. When states change and data has to be written, the rates will degrade to 1.1, 1.6 & 1.7 MHz respectively.
- Linux allows recording system utilization, specifically from CPU, RAM, network-IO & filesystem-IO
- Linux also allows recording synchronization stats from NTP, PTP and PHC2SYS

## Unittests

Unittests which also include loopback-tests. 
Data can be validated from fileInp - py - RAM - kernel module - cache - PRU - RAM - python sheep - fileOut

## Virtual Source

Why and how can you build trust?

battery OK is recorded together with GPIO 

virtual source is PRU. C-Code shared lib, Py
Py-port, virtual targets - similar to simba.
https://github.com/LENS-TUGraz/simba
With the addition that it's design can run in real-time with hardware in the loop.

## Time Synchronization

not the absolute time
only relative





TODO: add changelog


## 