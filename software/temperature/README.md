# Temperature acquisition — recovered versions

- `leitor_lm35_calibrado_v1.py` applies the **preliminary** cross-calibration `T_corrigida = 3.69 * T_firmware + 40.36`, dated 16 August 2026. It is not a definitive LM35 calibration and should not be used for absolute temperature claims without a reference validation.
- `leitor_meteo_v10.py` already exists in the repository at [software/acquisition/leitor_meteo_v10.py](../acquisition/leitor_meteo_v10.py); it is preserved there, not duplicated.
- Earlier METEO versions (V7–V9) and serial-reader prototypes (V1–V6) remain in the supplied local ZIP pending full historical archival.

These scripts assume a serial port such as `COM5`, which must be adapted to the connected Arduino.
