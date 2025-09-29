# Getting started

The testbed can be used via the [public web-API](/content/faq.md#web-api).
For easier access we provide a testbed-client and additional tooling written in Python.
This section will describe a typical workflow.

```{note}
If you have trouble recreating a setup please don't hesitate [contacting](/about/contact.md) us.
We are also thankful for [bugreports](/content/help_me_help_you).
```

## Installing the Tools

The tooling for the testbed is bundled in a package called `shepherd-data`.
Sources are [hosted on GitHub](https://github.com/nes-lab/shepherd-tools) and the package is [distributed via PyPI](https://pypi.org/project/shepherd-data/).

Tools: [![PyPI-Version](https://img.shields.io/pypi/v/shepherd_data.svg)](https://pypi.org/project/shepherd_data)


Client: [![PyPIVersion](https://img.shields.io/pypi/v/shepherd_client.svg)](https://pypi.org/project/shepherd_client)

You can install the user-tools & and client by using the package-manager of your choice.
In the following case we use pip:

```Shell
pip3 install shepherd-data -U
pip3 install shepherd-client -U
```

The user-tools contain

- data-models for configuring an experiment,
- reader and writer for the hdf5-files
- various functionality for analyzing the resulting hdf5-files, i.e. extraction, down-sampling, plotting
- a command-line interface (`shepherd-data` itself)
- simulators for the virtual source, including virtual harvesters
- waveform decoder (gpio-state & timestamp) for UART
- much more (out of scope for this guide)

## Defining an Experiment

Configurations are done with the help of Pydantic datamodels.
Most fields have sensible or neutral default values that can be omitted when designing an experiment.
The input data is automatically type-casted & validated and the resulting config can be easily imported & exported.
Users of FlockLab should quickly feel at home, as shepherds options are largely based on the well established FlockLab-config.

```{tip}
1) If you use an IDE and have the tooling installed, you can easily jump to the source of the data-class and see its defaults (i.e. `ctrl`-key + click on the class).
2) This is just ONE way of doing things. Configuration could be also done in [YAML-files](https://github.com/nes-lab/shepherd-tools/blob/main/shepherd_core/examples/experiment_from_yaml.yaml) or in JSON via the open web-API in your language of choice.
3) The API-documentation is integrated into the [main shepherd-documentation](https://nes-lab.github.io/shepherd/api/core_config.html)
3) While we work on a proper in-depth documentation, you can also [access the data-models online](https://github.com/nes-lab/shepherd-tools/tree/main/shepherd_core/shepherd_core/data_models)
```

Let's have a look at a minimal example that reuses an existing firmware:

```{literalinclude} getting_started_xp1.py
:language: python
:start-after: start example
:end-before: end example
:linenos:
```

This code will produce a valid run on the Testbed and capture a link-matrix.
But what is actually essential here?
Every experiment needs a **name** (`line 4`) and at least one element in the list of target configurations (`line 7-11`).
A **duration** (`line 5`) is used to limit the runtime and could be omitted.
In that case the duration of the energy environment is limiting the run.

When looking at the one **target configuration** group, we see that

- a list of **target IDs** is selected (`line 8`) for that group
- an **energy environment** is specified by name (`line 9`)
- also uses a pre-existing **firmware** (`line 10`) and
- **UART-logging** is activated (`line 11`) with its default config

This style of configuration allows you fully customize the experiment to your needs.
To give you some ideas:

- each target could be put in their own group and receive a custom environment, firmware and set of tracers
- this programmatic way makes it easy to run a parameter sweep via a range of experiments

### More advanced Example

To give you some additional common configuration options we have a look at a second, slightly more complex, experiment:

```{literalinclude} getting_started_xp2.py
:language: python
:start-after: start example
:end-before: end example
```

Compared to the first experiment the first target config group used just a subset of the target-nodes and assigns **custom IDs**.
These IDs will be patched into the firmware if possible.
More on that topic in the [next subsection](#adapting-the-firmware).

In addition to the environment a **virtual power source** is configured.
The first example omitted that, so the default was to switch into `direct`-mode and set the provided voltage of the environment as input for the target.
This time the experiment requests the emulation of a diode & capacitor - setup.
So instead of directly setting the target-voltage, the energy in the provided environment charges a virtual capacitor through a diode and then feeds the target from it.

Please note that the configuration of the virtual power source can range from simple to highly complex.
This will be explained more in depth in [its own section](/content/virtual_source.md).
We keep it simple by offering a predefined set of configurations that can be selected by name (i.e. `BQ25504`, `BQ25570`).
It is possible to customize single or more parameters with the same call.
The example demonstrates that by setting the storage capacitor to 100 uF.

The **firmware** is user-provided and will be embedded from the specified path into the resulting config.
Omitting the firmware-parameter flashes a default firmware to the target.
Looking into the data-model reveals the existenz of a `firmware2`-parameter for the MSP430-MCU.
To minimize the impact during an experiment a deep-sleep firmware is flashed.

While the first example only used the UART-logging, we see two additional tracers here.
The **power-tracer** records the energy consumption of the target.
Voltage & current are each sampled with 100 kHz.
This results roughly in a 1 MB/s datastream.

The second tracer records all GPIO-changes and acts like a logic analyzer.
Sampling is done at roughly 1.2 MHz and changes on any GPIO-pin will be saved with the exact timestamp.
To avoid sampling the UART-Pins (GPIO 0 & 1), they are taken out (masked) of the list of sampled GPIO.
The numbering of this list corresponds with the [GPIO-names of the target-port](/content/targets.md) and include 16x GPIO and two power-good-signals.

```{note}
1) Due to limited bandwidth of the filesystem it is only possible to continuously sample ~ 400 kSamples/s with a buffer that can hold burst with 3 MSamples.
Each observer monitors the backpressure and discards GPIO-Samples if certain thresholds are passed to ensure a responsive system.
2) The target-port holds more GPIO than the current shepherd-hardware can process.
It will be either [9x GPIO & PowerGood-High](https://github.com/nes-lab/shepherd-targets/tree/main/hardware/shepherd_nRF_FRAM_Target_v1.3e#connections-to-cape-v24-via-adapter) for now or [12x GPIO & 2x PowerGood](https://github.com/nes-lab/shepherd-targets/tree/main/hardware/shepherd_nRF_FRAM_Target_v1.3e#nrf52--msp430-fram-target-v13e) after the [expansion](/content/deployment.md#changes-in-near-future).
```

Thirdly the already known **UART-logger** is used with a custom baudrate.
This logger does not sample the GPIO itself, but uses the serial-interface provided by Linux.
Each received text-line gets timestamped and saved.
Due to the decoding, the datastream is smaller in comparison to the GPIO-tracer.
Unfortunately the interface produces a large CPU-overhead with higher baudrates.
That's why the rate is limit to 460800 baud.

```{tip}
If you wish to use higher baudrates with short burst-messages, you can use the GPIO-Tracer and decode UART later via the provided waveform-decoder.
The decoder can estimate serial configuration (baudrate, parity, stop-bits, ..) and produce a timestamped symbol-stream that can also be reduced to timestamped lines and whole text-blocks.
See [this example](https://github.com/nes-lab/shepherd-tools/blob/main/shepherd_core/examples/uart_decode_waveform.py) for details.
```

Lastly the second example defines an **additional target-config** that selects a small set of two targets.
For non-consecutive IDs the selection can be specified via the list-notation `[1, 4, 7]` instead of `range()`.
You can also see, that **no tracer** was configured here.
This is a rare, but still valid configuration-option.

```{attention}
TODO:
- Explain were to find existing content like eenvs, virtual sources,
- introduce testbed with an even simpler hello-world?
```

## Reduce Size of Result-Files

To give more control to the user, the experiment configuration includes several options for adjusting what is recorded and how it is post-processed.
This short guide can be useful to optimize download-durations, local storage constraints or simply getting by with the storage quotas of the testbed.
By default, no loggers or recorders are active as they are all opt-in.

Let's look at some numbers to bring the 200 GiB storage quota into perspective.
Depending on the use-case this can either hold 1 hour or several hundred hours of recordings.
`GPIOTraces` produce 10 bytes per sample (2 byte value, 8 byte timestamp).
So the sample-stream of continuous UART with 115 kBaud from the target results in roughly 1.2 MB/s.
`PowerTraces` are in a similar ballpark with 16 bytes per sample (2*4 byte value, 8 byte timestamp).
Shepherds sample-rate of 100 kHz produces 1.6 MB/s of data per node.

Here are some options to adjust the recording-behavior:

- GPIO- and Power-tracers can each be limited to a specific timeframe via the `delay` & `duration` argument, or be disabled completely
- The output of the Power-tracer can be set to only include power. Voltage and current are combined via `PowerTracing(only_power=True)`.
- The sample-rate of the Power-tracer can be adjusted, like `PowerTracing(samplerate=100)`. Caution is advised, as this setting will result in invalid data when used for I & V recording with a non-constant target voltage.
- a UART-logger can directly decode the GPIO-stream and only timestamps a line of text
- when combining GPIO-tracer and UART-logger, the UART-pins can be removed from the GPIO-tracer (in short `GpioTracing(gpios=range(2, 18)`)

If quota hits, note that user-data can be deleted from the testbed-server, even without downloading it first.

## Adapting the Firmware

While the testbed offers two target ports per observer, only one port is occupied at the moment.
The target is fully open source and features an nRF52 and msp430.
A [separate targets-repository](https://github.com/nes-lab/shepherd-targets/tree/main?tab=readme-ov-file#nrf52-with-msp430fr-as-fram) holds more information:

- full feature-list and pictures
- schematics and other design-files
- firmware-examples (compiled binaries are auto-generated and included in each release)

The important part for adapting a firmware is the [table of shared pins](https://github.com/nes-lab/shepherd-targets/tree/main/hardware/shepherd_nRF_FRAM_Target_v1.3e#nrf52--msp430-fram-target-v13e) and [a template](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/nrf52_demo_rf/src/shepherd_node_id.c) for patching the node ID.

When an `elf`-firmware contains a ``SHEPHERD_NODE_ID``, the variable will be patched with the actual target-ID before running the experiment.
See the proposed [c-file](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/nrf52_demo_rf/src/shepherd_node_id.c) for more information.

```{note}
The nRF has no outer reset line!
Configuring one could keep the MCU in permanent reset.
Code for the nRF52-DK may use P0.21 for reset.
This pin is actively used for UART-Rx here.
```

```{attention}
TODO: description of targets now has [its own sub-page](/content/targets.md).
```

## Scheduling an Experiment

The testbed-client can be used to connect with the testbed-server remotely.
During upload, the experiments get more deeply validated, also considering the current structure of the testbed.
When the configuration passes an experiment-ID is returned.
That ID can then be used to schedule the experiment.

```{literalinclude} getting_started_xp_schedule.py
:language: python
:start-after: start example
:end-before: end example
```

Upon submitting an experiment a set of tasks is created and scheduled:

- first the node IDs are patched into the firmwares (optional, when `ELF` was provided)
- secondly the targets are programmed with the firmware
- now it's possible to run the actual experiment
- a cleanup-task collects the data and prepares the download

Each Observer generates a hdf5-file that can be later downloaded.
You will be informed via e-mail when the download is ready.
If the `email_results` option in the experiment-config is disabled, e-mails will only be sent if all scheduled experiments finished or if the experiment had an error during execution.

Keep in mind, that you don't need to remember specific IDs as they can be always queried.
The following snippet schedules all (previously unscheduled) experiments:

```{literalinclude} getting_started_xp_schedule.py
:language: python
:start-after: start extra
:end-before: end extra
```

## Getting the Data

Information about the experiments stored on the testbed can be queried via:

```{literalinclude} getting_started_xp_info.py
:language: python
:start-after: start example
:end-before: end example
```

The command `.list_experiments()` returns a dictionary with the ID as key and the current state as value.
The ID can then be used to request the whole experiment-configuration.

Analog to that approach it is possible to use the ID for downloading and deleting specific experiments:

```{literalinclude} getting_started_xp_download.py
:language: python
:start-after: start example
:end-before: end example
```

Files will be created in a subdirectory with the pattern `SchedulingTimestamp-ExperimentName` and are then ready for analysis.

## Analyzing the Results

`Shepherd-data` offers a powerful CLI-interface that makes accessing the data inside the `hdf5`-files easy.
It is possible to extract data & logs, calculate metadata and generate plots.
Analyzing the data can hardly be generalized, so this short guide will mostly help you get an overview.
Have a look at [the APIs](https://nes-lab.github.io/shepherd/api/data_hdf5.html) of `shepherd-core` and `shepherd-data` to get a more in-depth view.

```{note}
The tool has integrated help-functionality. For a full list of supported commands and options, run `shepherd-data --help` and for more detail on a single command: `shepherd-data [COMMAND] --help`.
```

To get a basic overview, let's extract UART-logs and meta-data first. The following commands can be applied to single files, whole directories (`.`) or even go down into subdirectories (`--recurse`).

```Shell
# executed in your downloaded experiment-directory
shepherd-data extract-uart .
shepherd-data extract-meta .
```

The second command will generate `.yaml`-files showing the data contained in the files.
While a basic structural overview is given in the [main-docs](https://nes-lab.github.io/shepherd/user/data_format.html), this exposes all contained data.
For voltage and current recordings it even compiles some statistics.
Full system logs can be extracted by adding the `--debug`-switch.

When PowerTracing was included, plots can be generated via:

```Shell
# overview, with one plot per file
shepherd-data plot .
# detailed plot, including all files
shepherd-data plot . --start 10 --end 15 --multiplot
```

The second command will combine all sub-plots into one plot and limit the time-axis to a 5 seconds window, starting at 10 s.
