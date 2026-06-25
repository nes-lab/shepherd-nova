# Targets

This page introduces the available targets for the testbed.
In addition, we show how to

- migrate to our hardware,
- use the automatic node-ID patching, and
- inform about possible pitfalls.

But first some words about the interface between targets and the observer.
One of our design goals was to make features as neutral as possible.
What does that mean?
Using a feature like GPIO-Tracing shouldn't have a meaningful impact on power-tracing, beside keeping the microcontrollers up for controlling the GPIO itself.
Our level translators have a high impedance input and the traces itself have low capacitance for low energy losses during GPIO-usage.
We went a step further and made sure that disabled features have even less of an impact.
To continue with the GPIO topic - analog switches with a very low leakage current (in the nano-amp-scale) are used to separate GPIO traces from the observer if the feature is not in use.
This way users with sensitive power-measurements can make sure that the results are least skewed.

```{note}
Shepherd Nova has a second (unused) target-port on each observer and our team is [looking for ideas](https://github.com/nes-lab/shepherd-targets/issues/68).
```

## nRF52 with MSP430FR as FRAM

The current hardware v1.3+ uses

- Nordic nRF52840 - primary MCU with RF
- TI MSP430FR5994 - secondary MCU with low-energy persistent memory
- Abracon AB1805 - real-time clock

The main microcontroller for the user is the nRF52840.
It is widely used in the community and offers a powerful radio.
The MSP430 on the other hand offers a fairly large FRAM for intermittent computing.
Using both controllers with custom firmware is possible.
For ease of use we provide a firmware to use the MSP430 as an SPI flash storage.
Users can also completely ignore the MSP430 and its features.
If no firmware is selected, the testbed automatically disables the controllers by flashing a deep-sleep-firmware.

```{figure} /media/shepherd_nRF_FRAM_Target_v1.3_photo_front.jpg
:align: center
:alt: Front of Target PCB v1.3e

Photo of Target PCB v1.3e
```

BOM, gerber-files and schematics are available in the [PCB-Directory](https://github.com/nes-lab/shepherd-targets/tree/main/hardware).

To quickly port your existing firmware to our hardware, we provide a handy mapping of [shared pins below](#shared-pins).
For the initialization phase it may be beneficial to check the init-code of our [example-firmwares](#firmwares).

### Features

- freedom to use both MCUs as needed (just as radio or FRAM) or disable when not needed (deep sleep)
- over-voltage protection for V_LV (max 3.9V)
- under-voltage protection with hysteresis for nRF
- one debug LEDs with separate supply for minimal impact on pwr-budget
- one self-powered LED to "burn" energy
- io pins not interfering with RF (nRF PS v1.6 page 578)
- LEDs / UART similar to [Riotee](https://www.riotee.nessie-circuits.de/)
- nRF uses low voltage mode (PSv1.1 page 61)
- 16x GPIO shared to host, current-limited with 240R star-configuration (every participant has that resistor on its port to also keep data rates >10 MHz)
- high & low power-good-signal (similar to Riotee)
- SMA-port for external antenna
- RF-Balun optimized for high output power (PS v1.8 ref circuit 7)

### Shared Pins

The table below lists all shared pins between MCUs and Observers with **Cape V2.5**.

| Tgt-Port | Dir   | Riotee     | nRF52  | msp430  | Description                 |
|----------|-------|------------|--------|---------|-----------------------------|
| GPIO0    | <-A-> | GPIO.0     | P0.21  | P2.6    | UART Target-RX, msp.A1.CiPo |
| GPIO1    | <--   | GPIO.1     | P0.08  | P2.5    | UART Target-TX, msp.A1.CoPi |
| GPIO2    | <-B-> | GPIO.2     | P0.04  | P2.3    | msp.A1.PSel                 |
| GPIO3    | <-B-> | GPIO.3     | P0.05  | P2.4    | msp.A1.CLK                  |
| GPIO4    | <-C-> | GPIO.4     | P1.09  | P4.6    |                             |
| GPIO5    | <-C-> | GPIO.5     | P0.26  | P3.6    |                             |
| GPIO6    | <-C-> | GPIO.6     | P1.03  | PJ.6    |                             |
| GPIO7    | <-C-> | GPIO.7     | P0.11  | P5.3    | msp.B1.PSel                 |
| GPIO8    | <--   | GPIO.8     | P0.13  | P5.2    | msp.B1.CLK                  |
| GPIO9    | <--   | GPIO.9     | P0.16  | P5.1    | msp.B1.CiPo                 |
| GPIO10   | <--   | -          | P0.12  | P5.0    | msp.B1.CoPi, SDA            |
| GPIO11   | <--   | -          | P0.10  | P6.0    | msp.A3.CoPi, TXD            |
| (GPIO12) | <--   | -          | P0.19  | P6.1    | msp.A3.CiPo, RXD            |
| (GPIO13) | <--   | -          | P0.20  | P6.3    | msp.A3.STE                  |
| (GPIO14) | <--   | -          | P0.24  | P6.6    | msp.A3.CLK                  |
| (GPIO15) | <--   | -          | P0.27  | P6.7    | msp.A3.STE                  |
| PwrGoodL | -->   | PG_L       | P0.23  | P5.4    |                             |
| PwrGoodH | -->   | PG_H       | P0.07  | P5.5    |                             |
| prog11   | -->   | SWD.CLK    | swdclk | -       |                             |
| prog12   | <-D-> | SWD.IO     | swdio  | -       |                             |
| prog21   | -->   | SBW.CLK    | -      | sbwtck  |                             |
| prog22   | <-E-> | SBW.IO     | -      | sbwtdio |                             |
|          | -     | LED.0      | P1.13  | P5.7    |                             |
|          | -     | LED.2P     | P0.03  | PJ.0    |                             |
|          | -     | I2C.SCL    | P1.08  | P6.5    |                             |
|          | -     | I2C.SDA    | P0.06  | P6.4    |                             |
|          | -     | RTC.INT    | P0.30  | P7.3    | shared, no fct for shp      |
|          | -     | MAX.INT    | P0.25  | PJ.1    | shared, no fct for shp      |
|          | -     | C2C.CLK    | P0.18  | P1.5    | msp.A0.CLK                  |
|          | -     | C2C.CoPi   | P0.17  | P2.0    | msp.A0.CoPi                 |
|          | -     | C2C.CiPo   | P0.14  | P2.1    | msp.A0.CiPo                 |
|          | -     | C2C.PSel   | P0.22  | P1.4    | msp.A0.PSel                 |
|          |       | C2C.GPIO   | P0.15  | PJ.2    |                             |
|          |       | THRCTRL.H0 | P0.09  | P1.3    | shared, no fct for shp      |
|          |       | THRCTRL.H1 | P1.02  | P3.3    | shared, no fct for shp      |
|          |       | THRCTRL.L0 | P1.07  | P6.2    | shared, no fct for shp      |
|          |       | THRCTRL.L1 | P1.04  | P7.0    | shared, no fct for shp      |
|          |       | VCAP.Sense | P0.29  | P7.5    | VTarget                     |

**Note**:

- GPIO12 to GPIO15 are not recordable by the testbed with cape V2.5, as pins on the SBC are all used up
- The nRF has no outer reset line - so configuring one could keep the MCU in permanent reset. Code for the nRF52-DK may use P0.21 for reset - it is actively used for UART-Rx here.
- A, B, C in DIR-Column refer to switch-groups. 1, 2 and/or 4 bits can be reversed to talk to the target.
- D, E are switch-groups needed for programming

### Firmwares

#### nRF52

- [nrf52_demo_rf](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/nrf52_demo_rf): demo implementation for a simple node that sends BLE packets when energy budget allows it
- [nrf52_testable](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/nrf52_testable): watches all gpio and reports with UART messages (verification after assembly)
  - ensures that pcb is assembled OK and both MCUs are programmable and show basic functions
  - what is not tested: watchdog, FRAM, RF-Frontend (-> use rf-demo or rf-survey), sleep power consumption
- [nrf52_rf_test](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/nrf52_rf_test): sends out 1 BLE-Packet per second (verify with an app like `RaMBLE`)
- [nrf52_rf_survey](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/nrf52_rf_survey): Link Matrix Generator - TX-Unit - sends packet with every possible P_TX, loops until stopped
- [nrf52_deep_sleep](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/nrf52_deep_sleep): practically turned off MCU with the lowest possible consumption

#### MSP430FR

- [msp430_deep_sleep](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/msp430_deep_sleep): practically turned off MCU with the lowest possible consumption
- [msp430_spi_fram](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/msp430_spi_fram): [riotee](https://github.com/NessieCircuits/Riotee_MSP430Fram) implementation to use MSP as a flash storage
- [msp430_testable](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/msp430_testable): switches on all shared gpio one by one (verification after assembly)

## Custom Node ID

Developers of communication protocols often rely on unique IDs in their network.
While it might be possible to use the embedded UUID of the microcontroller itself, it has advantages to provide a custom ID for each target device.
To avoid providing a dedicated firmware for each MCU our testbed offers to automatically patch generic firmwares before being flashed.

When an `elf`-firmware contains a ``SHEPHERD_NODE_ID``, the variable will be patched with the actual target-ID before running the experiment.
This will be either the target-ID of the testbed (see [floor-plan](/content/deployment.md#floor-plan)) or the custom ID (if provided).
See the proposed [c-file](https://github.com/nes-lab/shepherd-targets/tree/main/firmware/nrf52_demo_rf/src/shepherd_node_id.c) for more information.

## References

1) Main Target-Repo & General Overview: <https://github.com/nes-lab/shepherd-targets/>
2) Target-Port of current Cape v2.5e: <https://github.com/nes-lab/shepherd/tree/main/hardware/cape_v2.5e#target-port---cape-25d-this-revision>
3) Main-Doku & general Overview (same as above): <https://nes-lab.github.io/shepherd/external/readme_targets.html>
