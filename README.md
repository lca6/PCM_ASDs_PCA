# Principle Component Analysis on Raman spectra of Paracetamol Amorphous Solid Dispersions
This is the repository that accompanies the paper titled 'Material-sparing screening of amorphous solid dispersions using low frequency Raman spectroscopy'. You can read the paper in the pdf file titled ".pdf"

## Installation
1) Download this repository via `git clone`
2) Create a conda environment (download Miniconda at https://www.anaconda.com/docs/getting-started/miniconda/main)
3) Type `pip install .`
4) Create a .env file in the format:

```dotenv
MACBOOK_URL=path_to_your_directory
ANALYSIS_FOLDER=name_of_folder_for_analysis
PCA_OUTPUT=name_of_folder_for_txt_files_output_from_pca
SPECTRA_OUTPUT=name_of_folder_for_graphs
```

## Workflow
1) Activate the conda environment
1) Copy and paste the txt files that you want to analyse into ANALYSIS_FOLDER
2) Change any parameters you want in settings.py
3) Type `python pca.py` to create a pca model
4) Type `python spectra.py` to create desired graphs

## data_collected/
A folder containing txt files obtained from the HORIBA LabRAM Odyssey confocal Raman microscope.

## pyphi/
Folder containing files from Sal Garcia's pyphi repository (available at https://github.com/salvadorgarciamunoz/pyphi) which allow us to conduct PCA on the spectral data.
