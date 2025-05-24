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

[![PyPI-Version](https://img.shields.io/pypi/v/shepherd_data.svg)](https://pypi.org/project/shepherd_data)

It contains

- the testbed-client,
- data-models for configuring an experiment,
- various functionality for analyzing the resulting hdf5-files, i.e. extraction, down-sampling, plotting
- a command-line interface and
- much more (out of scope for this guide)

You can install the user-tools by using the package-manager of your choice.
In this case we use pip:

```Shell
pip3 install shepherd-data -U
```

## Defining an Experiment

Configurations are done with the help of Pydantic datamodels.
Most fields have sensible or neutral default values that can be omitted when designing an experiment.
The input data is automatically type-casted & validated and the resulting config can be easily imported & exported.
Users of FlockLab should quickly feel at home, as shepherds options are largely based on the well established FlockLab-config.

```{tip}
1) If you use an IDE and have the tooling installed, you can easily jump to the source of the data-class and see its defaults (i.e. `ctrl`-key + click on the class).
2) This is just ONE way of doing things. Configuration could be also done in [YAML-files](https://github.com/nes-lab/shepherd-tools/blob/main/shepherd_core/examples/experiment_from_yaml.yaml) or in JSON via the open web-API in your language of choice.
3) While we work on a proper in-depth documentation, you can [access the data-models online](https://github.com/nes-lab/shepherd-tools/tree/main/shepherd_core/shepherd_core/data_models)
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
- **UART-tracing** is activated (`line 11`) with its default config

This style of configuration allows you fully customize the experiment to your needs.
To give you some ideas:

- each target could be put in their own group and receive a custom environment, firmware and set of tracers
- this programmatic way makes it easy to run a parameter sweep via a range of experiments

### A more advanced Example

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

While the first example only used the UART-Tracer, we see two additional tracers here.
The **power-tracer** records the energy consumption of the target.
Voltage & current are each sampled with 100 kHz.
This results roughly in a 1 MB/s datastream.

The second tracer records all GPIO-changes and acts like a logic analyzer.
Sampling is done at roughly 1.2 MHz and changes on any GPIO-pin will be saved with the exact timestamp.

```{note}
Due to limited bandwidth of the filesystem it is only possible to continuously sample ~ 400 kSamples/s with a buffer that can hold burst with 3 MSamples.
Each observer monitors the backpressure and discards GPIO-Samples if certain thresholds are passed to ensure a responsive system.
```

Thirdly the already known **UART-Tracer** is used with a custom baudrate.
This tracer does not sample the GPIO itself, but uses the serial-interface provided by Linux.
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
TODO: description of targets now has its own sub-page.
```

## Scheduling an Experiment

The testbed-client included in `shepherd-core` can be used to connect with the testbed-server remotely.
With an active connection the experiments get more deeply validated, also considering the current structure of the testbed.

```{attention}
TODO: add codesnippet and CLI-call to submit an experiment.
```

Upon submitting an experiment a set of tasks is created and scheduled:

- first the node IDs are patched into the firmwares (optional, when `ELF` was provided)
- secondly the targets are programmed with the firmware
- now it's possible to run the actual experiment
- a cleanup-task collects the data and prepares the download

Each Observer generates a hdf5-file that can be later downloaded.

## Getting the Data

```{attention}
TODO: add codesnippet and CLI-call to download an experiment.
```

## Analyzing the Results

`Shepherd-data` offers a powerful CLI-interface that makes accessing the data inside the `hdf5`-files easy.
It is possible to extract data & logs, calculate metadata and generate plots.

```{attention}
TODO: show access via python script and CLI, link to main doc for API
```
