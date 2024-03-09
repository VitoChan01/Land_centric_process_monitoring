# Seed_to_harvest_process_monitoring
**Seed-to-Harvest Process Monitoring using Remote Sensing**


Agricultural processes exhibit unique levels of complexity and risk. Challenges of monitoring these processes arise from the diversity of environmental factors that can hit a field at any time and the fuzziness of the actual state of the crop. Precise capabilities of monitoring the seed-to-harvest process provides benefits for the management activities of the farmer as well as for partners such as financial institutions.
In this paper, we address the unique challenges of agricultural processes. More specifically, we introduce a novel technique for monitoring seed-to-harvest processes by help of satellite sensors. We provide a proof-of-concept implementation and evaluate it in a case study on publicly available farm data from the United States. The evaluation demonstrates the viability of process mining as a technique for automatic monitoring of seed-to-harvest processes.

This repository contains the implementation of "Seed-to-Harvest Process Monitoring using Remote Sensing". The paper was submitted to BPM 2024.

## Dependencies
* Python 3.11+
## Required packages
* earthengine-api
* GeoPandas
* geemap
* Matplotlib
* Numpy
* Pandas
* PM4Py
* pyproj
* SciPy
## Structure
### Event_log
This directory contains the event log generated in this study.
### Source
This directory contains the codes of this implementation.
### Result
This directory contains the plots generated.
## Codes
### Implementation
- [Download time series data from Google Earth Engine](Source/GEE_download.ipynb)
- [Event log generation](Source/MACD_NDVI.ipynb)
- [Crop rotation prediction](Source/rotation_prediction.py)
### Evaluation
- [Performance spectrum](Source/pm4py_temporal.ipynb)
- [Smoothing assessment](Source/smoothing_effect.ipynb)
## Overview

## License 
[LICENSE](LICENSE)