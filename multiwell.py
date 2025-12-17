# This file loads in Raman spectra obtained using the multiwell function on a plate

# To be read, the files must be in the format [row][column].xy

# The spectral data can then be preprocessed and analysed using Principle Component Analysis (PCA)

# The spectra can also be visualised

import pandas as pd
import numpy as np
import pyphi as phi
import pyphi_plots as pp


import ramanspy as rp
import string
from parse import parse_csv

from dotenv import load_dotenv
import os

load_dotenv()

onedrive_url = os.getenv("ONEDRIVE_URL")

# A-H
rows = [x for x in string.ascii_uppercase[:8]]

# 1-12
columns = [x for x in range(1, 13)]

# list of raman spectra
samples = []

# e.g. A2, B7, C9
indices = []

for r in rows:
    for c in columns:
        
        # Loads the Raman spectra for visualising the spectra
        try:
            raman_spectrum = parse_csv(f"{onedrive_url}pca/pyphi/spectra_data/csv/{r}{c:02d}.csv")

        except FileNotFoundError:
            continue

        samples.append(raman_spectrum)

        indices.append(f'{r}{c}')

# Visualising the spectra
rp.plot.spectra(samples, label=None, title="Raman spectra", plot_type="single")

rp.plot.show()

