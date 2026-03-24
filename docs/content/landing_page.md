# Shepherd Nova

`Shepherd Nova` is the public instance of the Shepherd Testbed -
a distributed platform for rigorous experiments under repeatable energy-harvesting conditions.
In simpler terms, the testbed helps explore ways to eliminate the need for batteries and their potentially harmful chemistry.

## 🎉 Welcome!

If you're new here, don't worry — Shepherd Nova is designed to make advanced experiments simple and accessible. You get a professional test environment without the usual setup headaches.

Our system was presented at [MobiSys 2025](https://dl.acm.org/doi/10.1145/3711875.3729146) (the [23nd ACM International Conference](https://www.sigmobile.org/mobisys/2025/) on Mobile Systems, Applications, and Services). We're proud to offer this platform to researchers and developers like you.

Direct Link: <https://testbed.nes-lab.org/>

## ✨ What makes Shepherd Nova special?

### For Newcomers

- No hardware lab required — Access a professional testbed from your desk.
- [Guided Setup](content/getting_started.md) — No deep hardware knowledge required. We provide tools and documentation to get your first experiment running quickly.
- Everything included — From power management to logging, the testbed handles the heavy lifting.
- Focus on your code — Upload your firmware, define energy conditions, and let the system do the rest.

### For Professionals

- Precise & repeatable — Consistently replay real‑world energy environments across experiments.
- High‑fidelity measurement — Record voltage and current at 100 kHz, with sub‑microsecond timestamping.
- Flexible I/O — Capture GPIO signals up to 1 MHz, decode UART, and more.
- Smart supervision — An extensive system monitors and diagnoses every critical element during operation, embeds the logs in the results and therefore creates a new level of transparency.

## 🧪 Testbed capabilities at a glance

- [10+ observer-nodes](/content/deployment.md) for distributed experiments
- [nRF52-Targets](https://github.com/nes-lab/shepherd-targets/) with an extra MSP430 (usable as FRAM for checkpointing)
- [Virtual power source](/content/virtual_source.md) for replaying energy environments
  - consistently replicate real-world spatio-temporal energy availability across multiple experiments
- record power traces at a rate of 100 kHz with separate values for current & voltage
- timestamping with sub-µs accuracy across the testbed
- GPIO capture (12 ch, up to 1 MHz), UART decoding, embedded logs
- Auto-patching of node-ID in `ELF` firmware
- tooling in and around the system (batteries included)

## 🚀 Get started in three steps

1. Read the documentation — We provide step‑by‑step guides for your first experiment.
2. Prepare your firmware — Build for nRF52 targets (MSP430 optional for advanced use).
3. Run your experiment — Define energy traces, upload, and collect results.

## 🛠️ What do I need?

- an email-account to [register your user-account](/content/account.md) for the testbed
- a host system that is capable of running python (v3.10 or newer)
- internet access to work with the web-API

## 📄 Learn more

- Paper — [Shepherd Nova at MobiSys 2025](https://dl.acm.org/doi/10.1145/3711875.3729146)
- Tools & SDK — Everything you need is available in [our repositories](https://github.com/nes-lab/shepherd-tools)
- Support — Questions are always welcome. Check our quick‑start guide or open an issue

## Sitemap
