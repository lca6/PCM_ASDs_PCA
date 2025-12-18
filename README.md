# Principle Component Analysis on Raman spectra of Paracetamol Amorphous Solid Dispersions
This is the repository that accompanies the paper titled 'Material-sparing screening of amorphous solid dispersions using low frequency Raman spectroscopy'.

The paper is available at [URL].

## analysis.py
This file loads in Raman spectral data.

The spectral data can then be preprocessed and analysed using Principle Component Analysis (PCA).

The spectra can also be visualised.

## spectra_data/
A folder containing .txt files obtained from the HORIBA LabRAM Odyssey confocal Raman microscope.

## spectra_data/input_files
A folder for all the .txt files that you want to be analysed.

## spectra_data/output_files
A folder for any files created after the input files are processed.

## pyphi.py | pyphi_batch.py | pyphi_plots.py
Files courtesy of Sal Garcia's pyphi repository (available at https://github.com/salvadorgarciamunoz/pyphi) which allow us to conduct PCA on the spectral data.

## Usage
1) Download this repository via ```git clone```
2) Install the raman, pyphi, pyphi_plots and pyphi_batch modules by opening a terminal window, navigating to the root of this repository, and typing ```pip install .```