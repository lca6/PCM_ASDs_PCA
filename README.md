# Principle Component Analysis on Raman spectra of Paracetamol Amorphous Solid Dispersions

## Overview
This is the repository that accompanies the paper titled 'Material-sparing screening of amorphous solid dispersions using low frequency Raman spectroscopy'. You can read the paper in `dissertation.pdf`

## Installation
1) Download this repository via `git clone`
2) Create a conda environment (download Miniconda at https://www.anaconda.com/docs/getting-started/miniconda/main)
3) Type `pip install .`

## Workflow
1) Activate the conda environment
1) Copy and paste the .txt files to be analysed into `analyse`
2) Configure parameters in `settings.py`
3) Type `python -m pcm_asds_pca.analysis.pca` to create a PCA model
4) Type `python -m pcm_asds_pca.analysis.spectra` to display desired graphs

## Output
The scripts in this project automatically generate output files in designated folders:

- `pca.py` outputs the PCA model to the folder `pca_output`

- `spectra.py` outputs graphs to the folder `spectra_output`

These folders are created automatically the first time you run the scripts.  

Inside the repository, the folders contain a `.gitkeep` file. This file is a placeholder to preserve the empty folder structure in Git, and will be replaced or supplemented by actual output files when you run the scripts.

### Customizing the Output Folder

You can modify the default output folders by editing `settings.py`:

## Project Structure
### data_collected/
A folder containing .txt files obtained from the HORIBA LabRAM Odyssey confocal Raman microscope.

### pcm_asds_pca/pyphi/
A folder containing files from Sal Garcia's pyphi repository (available at https://github.com/salvadorgarciamunoz/pyphi) which allow us to conduct PCA on the spectral data.

### pcm_asds_pca/analysis/
A folder containing `pca.py` and `spectra.py` for creating a PCA model and displaying graphs.

### pcm_asds_pca/config/
A folder containing `settings.py` to configure the PCA model.

### pcm_asds_pca/core/
A folder contains functions and classes utilised by `pca.py` and `spectra.py`