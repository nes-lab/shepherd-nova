# Shepherd Nova

`Shepherd Nova` is the public instance of the Shepherd Testbed -
a public testbed for rigorous experiments under repeatable energy-harvesting conditions.
In the second half of 2023 a semi-open instance of the Shepherd testbed went live.
The public access is scheduled to launch during the MobiSys 2025.

Direct Link: <https://testbed.nes-lab.org/>

The testbed offers:

- [10+ observer-nodes](/content/deployment.md) for distributed operation
- [nRF52-Targets](https://github.com/orgua/shepherd-targets/) with additional msp430 that can be used as FRAM
- consistently replicate real-world spatio-temporal energy availability across multiple experiments
  - replay of [energy environments](/content/environments.md) in combination with a
  - an energy harvesting-component called [virtual power source](/content/virtual_source.md) to supply power to the targets (optional)
- record 100 kHz power traces with separate I & V (optional)
- timestamping with sub 1us accuracy across the testbed
- recording of target-GPIO with up to 1 MHz and 9 / 12 Channels (optional)
- decoding of UART at configurable baud rate (optional)
- patching of node-ID in target-firmware (optional)
- embedded logs, including an extensive warning-system that supervises & diagnoses every critical element during operation
- tooling in and around the system (batteries included)

```{seealso}
A publication about Shepherd Nova can be found in the proceedings of the
23nd ACM International Conference on Mobile Systems, Applications, and Services ([MobiSys 2025](https://www.sigmobile.org/mobisys/2025/)).
```

```{caution}
TODO: add link to paper and also add citation proposal
```
