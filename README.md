# FSCV-Multi-Channel-Chip-Readout-Board-Repository

This repository contains the PCB design files for an IC testing board designed for comprehensive assessment of Integrated Circuits (ICs).

## Board Overview

- **FSCV Channels**: 8
- **Layers**:
  - Top Layer: Analog Signals
  - 2nd Layer: Gnd Plane
  - 3rd Layer: Power Lines
  - Bottom Layer: Digital Signals

![Alt Text](Figures/fscvit2.png)
![Alt Text](Figures/fscvit2_b.png)
## Features

- **Microcontroller Control**: The board is equipped with a microcontroller to manage and control input to the IC under assessment.

- **Analog Switches**: Analog switches, controlled by the microcontroller, regulate input to the IC for precise testing.

- **JTAG Connector**: A JTAG (Joint Test Action Group) connector is provided for programming and configuring the microcontroller and for communicating with the MCU via a computer application.

- **Minimized User Intervention**: The board is designed to minimize user intervention and is intended to be placed inside a Faraday cage for a controlled testing environment.