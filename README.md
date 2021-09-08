# OrgaQuant Beekman
This repository contains an integration of the OrgaQuant model (Kassis et al. 2019) combined with a tracking implementation and size calculations to track organoid size over time.

## Prerequisites
* Windows OS
* NVidia GPU with CUDA

## Installation
* Important note: the programs works best in the main disk (due to speed). So the location of the data and the models can be set in data.conf and models.conf 
* Go to https://github.com/UMCU-BeekmanLab/OrgaQuantBeekman/actions/ and open the latest version
* Download the OrgaQuantBeekman Artifact (on the main disk)
* Unpack the artifact
* Install the environment by using [install.bat](./install.bat)
* Set the location of the main data in data.conf
* Set the location of the models in models.conf
* Download the models of interest https://github.com/TKassis/OrgaQuant/releases/tag/v0.2 and place the .h5 file in models folder (set in models.conf)
* The program is now ready for use

## Data
Copy organoid data in the main folder (seperate folder per experiment within the main data folder). Main data folder is set in models.conf

## Config
First, per experiment the OrgaQuant settings can be configured and saved using [run-config.bat](./run-config.bat) that starts a Jupyter notebook.

## Batch run
After setting the config for each experiment (unique folder in data) the [run-batch.bat](./run_batch.bat) can be used to execute a batch run on a all data present in ./data. Check the your data folder forthe results and output and error logs.

## Acknowledgement
The basis of the organoid tracking in this application has been developed by R. Rodenburg https://github.com/rrodenburg/OrgaSwell

## References
Kassis et al., OrgaQuant: Human Intestinal Organoid Localization and Quantification Using Deep Convolutional Neural Networks. Sci. Rep. 9, 1–7 (2019) [open-access paper](https://www.nature.com/articles/s41598-019-48874-y)