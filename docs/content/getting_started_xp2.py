"""How-to for defining a custom experiment.

compared to first experiment, this one:

- used just a subset of the target-nodes and assigns custom IDs
- embeds local firmware in yaml (elf-support is currently linux-only)
- use all 3 tracing-options - just for demonstration purposes
- second target configuration uses list-style to select targets
"""

# start example
from pathlib import Path

import shepherd_core.data_models as sm

xp = sm.Experiment(
    name="meaningful_TestName",
    duration=180,
    target_configs=[
        sm.TargetConfig(
            target_IDs=range(2, 10),
            custom_IDs=range(7, 30),  # longer list is OK
            energy_env=sm.EnergyEnvironment(name="eenv_static_3000mV_50mA_3600s"),
            virtual_source=sm.VirtualSourceConfig(
                name="diode+capacitor", C_intermediate_uF=100
            ),
            firmware1=sm.Firmware.from_firmware(
                file=Path("./firmware_nrf.elf").absolute(),
            ),
            power_tracing=sm.PowerTracing(),
            gpio_tracing=sm.GpioTracing(),
            uart_tracing=sm.UartTracing(baudrate=57600),  # default is 115200
        ),
        sm.TargetConfig(
            target_IDs=[1, 11],
            energy_env=sm.EnergyEnvironment(name="eenv_static_3000mV_50mA_3600s"),
            firmware1=sm.Firmware.from_firmware(
                file=Path("./firmware_nrf.elf").absolute(),
            ),
        ),
    ],
)
# end example
xp.to_file("experiment_rf_survey.yaml")


# next steps:
# - copy to server:
#   scp ./experiment_generic_varX_tbt.yaml user@shepherd.cfaed.tu-dresden.de:/var/shepherd/content/
# - run with herd-tool:
#   shepherd-herd --verbose run --attach /var/shepherd/content/experiment_generic_varX_tbt.yaml
