# Local PASCO temperature datasets — inventory

The original local `PASCO.zip` was inspected on 17 October 2026. This table records the filenames and **data row counts** (excluding header). The files are retained in the original ZIP and are **not all uploaded here**.

| Original file | Rows | Status |
| --- | ---: | --- |
| dados_temperatura_2026-08-15_16-25-09.csv | 399 | Local |
| dados_temperatura_2026-08-15_16-30-51.csv | 487 | Local |
| pasco_lm35_calibrado_2026-08-16_21-55-31.csv | 251 | Local |
| pasco_meteo_2026-08-15_18-48-26.csv | 0 | Header only |
| pasco_meteo_2026-08-15_18-49-08.csv | 0 | Empty (0 bytes) |
| pasco_meteo_2026-08-15_18-51-10.csv | 364 | Local |
| pasco_meteo_v8_2026-08-15_18-57-11.csv | 441 | Local |
| pasco_meteo_v9_2026-08-15_19-02-17.csv | 514 | Local |
| pasco_meteo_v10_2026-08-15_19-08-10.csv | 560 | Local |
| pasco_meteo_v10_2026-08-16_21-25-47.csv | 182 | Local |
| pasco_meteo_v10_2026-08-16_21-36-11.csv | 270 | Local |
| pasco_meteo_v10_2026-08-16_21-42-46.csv | 470 | Local |
| pasco_meteo_v10_2026-08-16_21-44-57.csv | 543 | Local |
| pasco_meteo_v10_2026-08-16_21-47-38.csv | 351 | Local |
| pasco_meteo_v10_2026-08-16_21-59-40.csv | 152 | Local |
| pasco_meteo_v10_2026-08-16_22-00-43.csv | 270 | Local |
| pasco_meteo_v10_2026-08-16_22-03-11.csv | 272 | Local |
| pasco_meteo_v10_2026-08-19_15-45-04.csv | 249 | Local |
| pasco_meteo_v10_2026-08-19_18-13-50.csv | 99 | Local |

The zero-byte and header-only files should be kept in the raw archive as evidence of acquisition attempts, but need not be treated as successful experiments. No calibration or scientific validation follows solely from these row counts.

## Data preservation recommendation
When publishing, retain original filenames and raw readings, include SHA-256 checksums, and never silently overwrite the original files. For analysis, use separate derived files and document the transformations.
