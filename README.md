# Principle Component Analysis on Raman spectra of Paracetamol Amorphous Solid Dispersions

## Overview
This is the repository that accompanies the paper titled 'Material-sparing screening of amorphous solid dispersions using low frequency Raman spectroscopy'. You can read the paper in `dissertation.pdf`. This repository is a fork of Sal Garcia's pyphi repository available at https://github.com/salvadorgarciamunoz/pyphi.

## Installation
3) Create and activate a conda environment (download Miniconda at https://www.anaconda.com/docs/getting-started/miniconda/main)

2) Clone this repository:
   ```bash
   git clone https://github.com/lca6/PCM_ASDs_PCA
   ```

3) Install the conda-only dependency required by `ramanspy`:
   ```bash
   conda install -c conda-forge cvxopt
   ```

4) Install this package and its pip-only dependencies:
   ```bash
   pip install ".[ramanspy]"
   ```

5) Rename `sample.env` to `.env`:
   ```bash
   mv sample.env .env
   ```

6) Populate the `PATH_TO_DIR` environment variable

## Workflow
1) Copy and paste the .txt files to be analysed into `analyse/`

2) Configure parameters in `settings.py`

3) To create a PCA model:
   ```bash
   pcm-asds-pca
   ```

4) To display desired graphs:
   ```bash
   pcm-asds-spectra
   ```

## Output
The scripts in this project automatically generate output files in designated folders:

- `pca.py` outputs the PCA model to `pca_output/`

- `spectra.py` outputs graphs to `spectra_output/`

`analyse/`, `pca_output/` and `spectra_output/` contain `.gitkeep` files. These files are placeholders to preserve the empty folder structure in Git. You can safely remove the `.gitkeep` files once you have cloned the repository.

### Customising the output folder names

You can modify the default output folder names by editing `settings.py`

## Project Structure
#### data/
Contains .txt files obtained from the HORIBA LabRAM Odyssey confocal Raman microscope.

#### pcm_asds_pca/
Contains all the project source code.

#### pcm_asds_pca/analysis/
Contains `pca.py` and `spectra.py` for creating a PCA model and displaying graphs.

#### pcm_asds_pca/config/
Contains `settings.py` to configure the PCA model.

#### pcm_asds_pca/core/
Contains functions and classes utilised by `pca.py` and `spectra.py`

#### pcm_asds_pca/pyphi/
Contains files from Sal Garcia's pyphi repository which allow us to conduct PCA on the spectral data.
