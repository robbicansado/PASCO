# PASCO

**Open-Source Data Acquisition Platform for Undergraduate Physics Laboratories**

> Undergraduate research project developed at the Institute of Physics of the University of São Paulo (IFUSP).

---

## About

PASCO is an undergraduate research project that aims to develop an open-source data acquisition platform for experimental physics laboratories.

The project combines Arduino-based hardware with a Python desktop application to acquire, visualize and export experimental data in real time, providing a flexible and low-cost alternative for educational laboratory activities.

---

## Objectives

- Develop a modular data acquisition platform.
- Create an intuitive graphical interface for laboratory use.
- Support multiple experimental sensors.
- Enable real-time visualization and data export.
- Facilitate the use of open-source technologies in physics education.

---

## Current Status

🚧 Active Development

Current focus:

- Software architecture
- Graphical User Interface (GUI)
- Experimental validation
- Documentation

---

## Repository Structure

```
PASCO/
│
├── docs/              # Documentation
├── firmware/          # Arduino firmware
├── software/          # Python application
├── hardware/          # Hardware documentation
├── data/              # Example datasets
└── README.md
```

---

## Technologies

- Python
- Arduino
- PySerial
- Matplotlib
- Tkinter

---

## Roadmap

- [ ] Interface V8
- [ ] Experimental validation
- [ ] Documentation
- [ ] Final report
- [ ] Public release

---

## Project Status

This repository is under active development as part of an undergraduate research project.

The documentation and source code will continue to evolve throughout the research period.

---

## Author

Robert Nicolas Duarte Bastos

Institute of Physics – University of São Paulo (IFUSP)

## Current Development Status — August 2026

The PASCO/FlexDuino project has entered a new experimental recovery and validation phase.

### Temperature subsystem

The first sensor subsystem investigated during this phase was temperature acquisition.

Current status:

- **FlexDuino central unit:** operational
- **Serial communication:** recovered and functional
- **Python acquisition environment:** functional
- **LM35:** partially validated; responds to thermal changes, but absolute calibration remains pending
- **METEO (AM2302/DHT22):** validated for temperature acquisition
- **Real-time visualization:** functional
- **CSV experimental recording:** functional
- **Current METEO software:** V10
- **Temperature experiment documentation:** completed

Experimental data and documentation are available in:

`experiments/temperature/2026-08-15/`

### Next development stage

With the initial temperature subsystem validated, development will proceed to the recovery and validation of sensors related to **movement and distance**, beginning with the ultrasonic sensor.

The current development strategy is to validate the available sensors individually before proceeding to multi-sensor integration and the construction of complete educational experiments.

---

## Supervisor

(To be added)
