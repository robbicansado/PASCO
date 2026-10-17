# Historical Python acquisition versions

This folder holds historical serial-reader scripts recovered from the local PASCO archive. They are **not** the recommended current application.

## Versions found in the original local archive
- `leitor_serial.py` — basic serial terminal reader (published here).
- `leitor_serial_v1.py.py` — another copy of the basic reader.
- `leitor_serial_v2.py.py` — serial parser for temperature and ultrasonic distance.
- `leitor_serial_v3.py` through `leitor_serial_v6.py` — historical experimental acquisition/plotting versions.
- `leitor_meteo_v7.py`, `leitor_meteo_v8.py`, `leitor_meteo_v9.py` — successive temperature acquisition versions.
- `leitor_meteo_v10.py` — already published at [software/acquisition/leitor_meteo_v10.py](../acquisition/leitor_meteo_v10.py).
- `leitor_lm35_calibrado_v1.py` — preliminary calibration at [software/temperature](../temperature/README.md).

Only the basic `leitor_serial.py` is added in this commit; the other historical source files remain in the original local archive pending verbatim transfer. Filename anomalies (such as `.py.py`) are part of the original archive and should be preserved or documented on import.
