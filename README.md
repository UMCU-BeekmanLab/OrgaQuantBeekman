# OrgaQuant Beekman
This repository contains an integration of the OrgaQuant model (Kassis et al. 2019) combined with a tracking implementation and size calculations to track organoid size over time.

## Installation
Run the following command to install the required packages in a conda environment:
```sh
conda env create -f conf/environment.yml
```
## Data
Copy organoid data in the ./data folder (seperate folder per experiment)

## Config
First, per experiment the OrgaQuant settings can be configured and saved using [run-config.bat](./run-config.bat) thats starts a Jupyter notebook.

## Batch run
After setting the config for each experiment (unique folder in data) the [run-batch.bat](./run_batch.bat) can be used to execute a batch run on a all data present in ./data. Check the your data folder forthe results and output and error logs.

## Acknowledgement
The basis of the organoid tracking in this application has been developed by R. Rodenburg https://github.com/rrodenburg/OrgaSwell

## References
Kassis et al., OrgaQuant: Human Intestinal Organoid Localization and Quantification Using Deep Convolutional Neural Networks. Sci. Rep. 9, 1–7 (2019) [open-access paper](https://www.nature.com/articles/s41598-019-48874-y)