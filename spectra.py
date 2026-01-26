import matplotlib.pyplot as plt
import ramanspy as rp

import sys
import pathlib
import re

from contextlib import redirect_stdout, redirect_stderr

from filter import (
    ROWS_TO_REMOVE,
    COLS_TO_REMOVE,
    MACBOOK_URL,
    ANALYSIS_FOLDER,
    WAVENUMBER_RANGE,
    sort_files,
)
from sample import Sample


# =======================
# Visualising the spectra
# ========================

files = pathlib.Path(ANALYSIS_FOLDER)
files = [str(x) for x in files.iterdir()]

# Confirm samples have been provided
try:
    files[0]
except IndexError:
    sys.exit("No files provided")

files, sample_labels = sort_files(files)

plate = []
spectra_to_visualise = []

for file in files:

    with open(file, encoding="latin-1") as f:
        text = f.read()

    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

    # Loads the Raman object for visualising the spectrum
    spectrum = rp.load.labspec(f"{MACBOOK_URL}{file}")

    sample = Sample(file, spectrum)

    plate.append(sample)

    # Filter spectra to be visualised
    if sample.row in ROWS_TO_REMOVE:
        continue
    elif sample.col in COLS_TO_REMOVE:
        continue

    # Crop spectra
    cropper = rp.preprocessing.misc.Cropper(region=WAVENUMBER_RANGE)
    spectrum = cropper.apply(sample.spectrum)

    spectra_to_visualise.append(spectrum)

with open("spectra_samples.txt", "w") as f:
    with redirect_stdout(f), redirect_stderr(f):
        for sample in plate:
            print(sample)

title = input("Title for Raman spectra: ")

rp.plot.spectra(
    spectra_to_visualise, label=sample_labels, plot_type="single", title="Raman spectrum "+title
)

plt.savefig(f"raman_spectrum_{title}")
plt.show()

print("Please see \"spectra_samples.txt\" for a list of the samples displayed.")
