# Temperature Validation — 15/08/2026

This experiment documents the recovery and initial validation of the temperature acquisition subsystem of the PASCO/FlexDuino project.

## Sensors tested

- LM35
- METEO module (AM2302/DHT22)

## LM35

The LM35 responded consistently to thermal stimuli, confirming that the sensor and acquisition chain are operational.

However, the absolute temperature values were incompatible with the conversion used by the recovered FlexDuino V5 firmware.

**Status:** Partially validated. Absolute calibration and conversion remain pending.

## METEO

The METEO module was connected directly to the FlexDuino ANALOG interface and produced plausible temperature measurements.

The system was tested under controlled thermal perturbations, including a 30–30–30 experimental protocol:

1. approximately 30 s at rest;
2. approximately 30 s under airflow;
3. recovery after removal of the airflow.

The experiment showed clear cooling followed by gradual thermal recovery.

**Status:** Validated for continued development.

## Acquisition software

The current reference implementation is **V10**.

It includes:

- real-time temperature acquisition;
- real-time plotting;
- raw and filtered temperature;
- moving median filtering;
- initial, minimum and maximum temperature;
- temperature variation (Delta T);
- estimated temperature variation rate;
- automatic thermal-state classification;
- automatic CSV recording.

## Experimental data

The `data/` directory contains the CSV dataset generated during the final METEO validation experiment.

The dataset preserves the experimental measurements for future analysis and reproducibility.

## Pending work

### LM35

- absolute calibration;
- determination of the correct conversion equation;
- validation against an external reference;
- future multi-sensor integration.

### METEO

- DB15 electrical pin mapping using a multimeter;
- identification of the secondary internal board;
- investigation of the external terminal;
- investigation of AM2302 humidity acquisition;
- quantitative validation of the V10 temperature-rate calculation.

These pending items do not block the next stage of development.

## Next stage

The next experimental subsystem to be investigated will involve **movement and distance measurement**, beginning with the ultrasonic sensor.
