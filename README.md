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

🚧 Active Development — optical acquisition milestone: 17 October 2026

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

### Optical subsystem — October 2026

The optical acquisition subsystem was reconnected and tested. The **A2** channel responds to illumination; **A1** remains unvalidated. PASCO Studio V0.1 demonstrated real-time plotting and data export.

- [Optical experiment (17 October 2026)](experiments/optical/2026-10-17/README.md)
- [Arduino optical diagnostic firmware](firmware/diagnostics/optical_a1_a2/optical_a1_a2.ino)
- [Ultrasonic Technical Report 09](docs/relatorios/Relatorio_09_Validacao_Comparativa_do_Sistema_Ultrassonico.pdf)

- [PASCO Studio V0.1 Python application](software/acquisition/pasco_studio_v01.py)
- [Optical acquisition CSVs and SVG graph](experiments/optical/2026-10-17/README.md#data-and-report)
- [Technical Report 10 LaTeX source](docs/relatorios/relatorio_10_pasco_optica.tex)

**Pending binary upload:** original optical PNG and compiled Report 10 PDF.

### Next development stage

Diagnose A1, verify A2 stability after power cycling, validate temperature acquisition within PASCO Studio, and work toward unified firmware while retaining validated legacy scripts.

---


### Recovered local archive — October 2026

Additional material recovered from the original PASCO working directory is now documented:

- [Ultrasonic Arduino diagnostic sketches](firmware/ultrasonic/README.md) — two sketches with different pin mappings and acquisition purposes.
- [Preliminary LM35 cross-calibration script](software/temperature/leitor_lm35_calibrado_v1.py) — provisional equation; absolute calibration still pending.
- [FlexDuino V5 firmware archive notes](firmware/legacy/README.md) — original binary/HEX backups retained locally pending exact binary transfer.

Historical serial-reader and METEO V7–V9 versions and selected temperature CSVs are awaiting archival. Existing METEO V10 and optical files remain unchanged.

---


### Local working-folder inventory — October 2026

The supplied local PASCO ZIP has been reviewed and organized without deleting or replacing validated sources:

- [Historical serial-reader versions](software/legacy/README.md) — basic reader published; remaining versions inventoried for exact archival.
- [Temperature CSV inventory](experiments/temperature/2026-08-15/LOCAL_ARCHIVE_INVENTORY.md) — 19 original files reviewed, including empty/incomplete acquisitions.
- [FlexDuino V5 firmware checksums](firmware/legacy/SHA256_LOCAL_ARCHIVE.txt) — checksum references for local original backups.

**Archive status:** This is an inventory and partial source-code transfer, not a complete mirror of the local PASCO ZIP. Large text disassemblies, firmware binaries, and remaining raw CSVs are still stored in the original local archive.

---

## Supervisor

(To be added)
