"""How-to for defining a custom experiment.

compared to first experiment, this one:

- used just a subset of the target-nodes and assigns custom IDs
- embeds local firmware in yaml (elf-support is currently linux-only)
- use all 3 tracing-options - just for demonstration purposes
- second target configuration uses list-style to select targets
"""

# start example
from pathlib import Path

import shepherd_core.data_models as sdm

xp = sdm.Experiment(
    name="meaningful_TestName",
    duration=180,
    target_configs=[
        sdm.TargetConfig(
            target_IDs=range(2, 10),
            custom_IDs=range(7, 30),  # longer list is OK
            energy_env=sdm.EnergyEnvironment(name="eenv_static_3000mV_50mA_3600s"),
            virtual_source=sdm.VirtualSourceConfig(
                name="diode+capacitor", C_intermediate_uF=100
            ),
            firmware1=sdm.Firmware.from_firmware(
                file=Path("./firmware_nrf.elf").absolute(),
            ),
            power_tracing=sdm.PowerTracing(),
            gpio_tracing=sdm.GpioTracing(gpios=range(2, 18)),  # exclude UART
            uart_logging=sdm.UartLogging(baudrate=57600),  # default is 115200
        ),
        sdm.TargetConfig(
            target_IDs=[1, 11],
            energy_env=sdm.EnergyEnvironment(name="eenv_static_3000mV_50mA_3600s"),
            firmware1=sdm.Firmware.from_firmware(
                file=Path("./firmware_nrf.elf").absolute(),
            ),
        ),
    ],
)
# end example
xp.to_file("experiment_rf_survey.yaml")
