# Principle Component Analysis on Raman spectra of Paracetamol Amorphous Solid Dispersions
This is the repository that accompanies the paper titled 'Material-sparing screening of amorphous solid dispersions using low frequency Raman spectroscopy'.

The paper is available at [URL].

## Installation
1) Download this repository via `git clone`
2) Activate a conda environment (download Miniconda at https://www.anaconda.com/docs/getting-started/miniconda/main)
3) Type `pip install .`

## Workflow
1) Create a .env file with the line `ANALYSIS_FOLDER="analyse"`
2) Copy the files from spectra_data/ that you want to analyse
3) Paste the files into to_be_processed/
4) Type `python3 *.py` where * is the name of the file you want to run to process the data

## spectra_data/
A folder containing .txt files obtained from the HORIBA LabRAM Odyssey confocal Raman microscope.

## pyphi/
Folder containing files from Sal Garcia's pyphi repository (available at https://github.com/salvadorgarciamunoz/pyphi) which allow us to conduct PCA on the spectral data.
