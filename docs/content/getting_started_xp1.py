"""How-to for defining a minimal experiment.

Minimal setup for measuring link matrix with pre-existing firmware

Assumptions:

- start ASAP,
- static Power-Supply
- use all 3 tracing-options - just for demonstration purposes
- second unused MCU gets sleep-firmware
"""

# start example
import shepherd_core.data_models as sdm

xp = sdm.Experiment(
    name="my_own_survey",
    duration=3 * 60,
    target_configs=[
        sdm.TargetConfig(
            target_IDs=range(1, 11),
            energy_env=sdm.EnergyEnvironment(name="eenv_static_3000mV_50mA_3600s"),
            firmware1=sdm.Firmware(name="nrf52_rf_survey"),
            uart_tracing=sdm.UartTracing(),  # default is 115200 baud
        ),
    ],
)
xp.to_file("experiment_rf_survey.yaml")
# end example
