# Principle Component Analysis on Raman spectra of Paracetamol Amorphous Solid Dispersions
This is the repository that accompanies the paper titled 'Material-sparing screening of amorphous solid dispersions using low frequency Raman spectroscopy'.

The paper is available at [URL].

## analysis.py
This file loads in Raman spectral data.

The spectral data can then be preprocessed and analysed using Principle Component Analysis (PCA).

The spectra can also be visualised.

## spectra_data/
A folder containing .txt files obtained from the HORIBA LabRAM Odyssey confocal Raman microscope.

## pyphi.py | pyphi_batch.py | pyphi_plots.py
Files courtesy of Sal Garcia's pyphi repository (available at https://github.com/salvadorgarciamunoz/pyphi) which allow us to conduct PCA on the spectral data.

## Usage
1) Download this repository via ```git clone```
2) Activate a conda environment (download Miniconda at https://www.anaconda.com/docs/getting-started/miniconda/main)
3) Type ```pip install .```