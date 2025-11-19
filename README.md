# Principle Component Analysis on Raman spectra of Paracetamol Amorphous Solid Dispersions
This is the repository that accompanies the paper titled 'Material-sparing screening of amorphous solid dispersions using low frequency Raman spectroscopy'. The paper is available at [URL].

## raman
The file for importing the Raman microscope data and conducting Principle Component Analysis on the spectra.

## spectra
A folder containing Raman spectra visualised using ramanspy (please see https://ramanspy.readthedocs.io/en/latest/)

## spectra_data
A folder containing .txt files obtained from the HORIBA LabRAM Odyssey confocal Raman microscope.

## pyphi | pyphi_batch | pyphi_plots | setup
Files courtesy of Sal Garcia's pyphi repository (available at https://github.com/salvadorgarciamunoz/pyphi) which allow us to conduct Principle Component Analysis on the spectral data

## Installation
1) Download this repository via ```git clone```
2) Install the raman, pyphi, pyphi_plots and pyphi_batch modules by opening a terminal window, navigating to the root of this repository, and typing 
```python -m pip install -r requirements.txt``` or ```python -m pip install .```