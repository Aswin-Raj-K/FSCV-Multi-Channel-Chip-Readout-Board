# FSCV-Multi-Channel-Chip-Readout-Board-Repository

This repository contains the PCB design files for an IC testing board designed for comprehensive assessment of Integrated Circuits (ICs).

## Board Overview

- **FSCV Channels**: 8
- **Layers**:
  - Top Layer: Digital Signals
  - 2nd Layer: Power Lines
  - 3rd Layer: Ground Plane
  - Bottom Layer: Analog Signals

![Alt Text](Figures/Full_Design.png)

## Features

- **Microcontroller Control**: The board is equipped with a microcontroller to manage and control input to the IC under assessment.

- **Analog Switches**: Analog switches, controlled by the microcontroller, regulate input to the IC for precise testing.

- **SMA Connectors**: SMA connectors are used for external inputs, ensuring efficient high-frequency signal exchange.

- **JTAG Connector**: A JTAG (Joint Test Action Group) connector is provided for programming and configuring the microcontroller.

- **Minimized User Intervention**: The board is designed to minimize user intervention and is intended to be placed inside a Faraday cage for a controlled testing environment.

<p align="center">
  <img src="Figures/PCB_TOP.png" alt="Board Top View" width="45%" />
  <img src="Figures/PCB_BOTTOM.png" alt="Board Bottom View" width="45%" />
</p>

<p align="center">
  <em>Figure 1: Board Top View</em> &emsp; <em>Figure 2: Board Bottom View</em>
</p>


