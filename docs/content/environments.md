# Energy Environments

The testbed offers a basic set of environments to satisfy most needs.
This section will guide you through the characteristics to help you make a choice for your experiments.

```{note}
We plan on extending this collection further in the near future.
If you have ideas, wishes or actual recordings please don't hesitate [contacting](/about/contact.md) us.
```

## Static Environments

A constant supply can be advantageous for various scenarios like debugging during firmware-development.
The testbed offers a set of 600 minute long recordings with:

- 2 or 3 V
- 1, 5, 10 or 50 mA

To select a static environment for an experiment the name can be derived like:

`eenv_stativ_{U\mV}mV_{I\mA}_{t\s}s`

So the trace with 3 V and 50 mA is selectable by name `eenv_static_3000mV_50mA_3600s`.

## Dynamic Environments

This sections contains artificial environments, beginning with on-off-patterns and ending with more complex simulated solar harvests.

```{attention}
WORK IN PROGRESS
```

```{tip}
Setting the virtual power source to `direct` will enable passthrough-mode.
The output-voltage for the target will directly react to the recording for truly replicating an on-off-pattern.
```

## Real-World Environment

Traces recorded with the shepherd harvester are currently based on the [published data](https://zenodo.org/records/6383042) of a prior paper.

```{attention}
WORK IN PROGRESS
TODO: differentiate single env to array of envs (=domain?)
```
