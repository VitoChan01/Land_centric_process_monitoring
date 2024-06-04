# Seed_to_harvest_process_monitoring
**Seed-to-Harvest Process Monitoring using Remote Sensing**

Cultivation processes can only be captured indirectly through information systems. Therefore, real-time monitoring of them is an open and complex challenge.
In this paper, we address the unique challenges of cultivation processes. More specifically, we introduce a novel technique to generate event logs of seed-to-harvest processes with the help of satellite data. We evaluate our approach using publicly available data from the United States. The evaluation demonstrates the viability of process mining as a technique for automatic monitoring of cultivation processes.

**Framework**
In this study we have developed a framework for monitoring agricultural business process through satellite.
![framework](Figure/framework_overview.png)
We have implemented our framework to investigate 15 years of agricultural activity from 2008 to 2022 on farm patches in Idaho, North Dakota, and Colorado, United States.


This repository contains the implementation of "Seed-to-Harvest Process Monitoring using Remote Sensing". The paper was submitted to ICPM 2024.

## Dependencies
* Python 3.11+
## Required packages
For required packages, please see [requirements.txt](requirements.txt).

To install all required packages: 
```
pip install -r requirements.txt
```
## Directories
### [Event_log](Event_log)
This directory contains the main results.
- `148sites_240129.xes`: Seed to harvest event log saved in xes format
- `log_148sites_240129_df.h5`: Seed to harvest event log saved in h5 format
- `transition_matrix.npy`: Estimated transition matrix for rotation prediction
### [Source](Source)
This directory contains the codes of this implementation.
## Codes
### Implementation
- `GEE_download.ipynb`: [Download time series data from Google Earth Engine](Source/GEE_download.ipynb)
    * To download data from GEE a GEE account is required. ([Sign up for GEE](https://earthengine.google.com/)) 
- `Eventlog_generation.py`: [Event log generation script](Source/Eventlog_generation.py)
- `Crop_prediction.py`: [Crop rotation prediction script](Source/Crop_prediction.py)
### Evaluation
- `Performance_spectrum_evaluation.py`: [Create performance spectrum](Source/Performance_spectrum_evaluation.py)
- `Smoothing_evaluation.py`: [Smoothing assessment](Source/Smoothing_evaluation.py)
- `Usual_dates.py`: [Comparison to usual dates](Source/Usual_dates.py)
### Modules
- `seed_to_harvest.py`: [MACD activity recognition and event log enrichment](Source/seed_to_harvest.py)
- `rotation_prediction.py`: [Markov chain rotation prediction](Source/rotation_prediction.py)
## Event log
The generated event log has the following attributes:
| Attribute | Description | Type |
|:----------:|:----------:|:----------:|
| Activity| Activity recognized | str |
| Timestamp| Timestamp filtered based on VI likelihood | pandas datetime object |
| Time_uncertainty| All valid recognition timestamp | list of pandas datetime object |
| CaseID| ID given to the case structured as xxxx_yyyy. The first 4 digit represent the ID given to the site and the last 4 digit represent the year of the case | str |
| Crop| Cultivated crop | str |
| SiteID| ID given to the farm patch | int |
| WGS84_lon_lat| Center coordinate of the farm patch (WGS84) | list |
| County| County in which the farm patch is located determined by WGS84 coordinate | str |
| State| State/province in which the farm patch is located determined by WGS84 coordinate | str |
| Country| Country in which the farm patch is located determined by WGS84 coordinate | str |
| NDVI_range| Max/min range of valid recognition NDVI | list |
| num_valid_est| Number of valid recognition(s) | int |
| Multiple_crop| Binary indicator of whether multiple crop type was detected on field. 0: only one type of crop was found. 1: more than one types of crop were found. | int |

## License 
[LICENSE](LICENSE)