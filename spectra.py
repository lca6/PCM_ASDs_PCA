import ramanspy as rp

import sys
import pathlib
import re

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

    sample = Sample()

    sample.get_sample_metadata(file, spectrum)

    plate.append(sample)

    # Filter spectra to be visualised
    if sample.row in ROWS_TO_REMOVE:
        continue
    elif sample.col in COLS_TO_REMOVE:
        continue

    # =============
    # Preprocessing
    # =============

    # Crop spectra
    cropper = rp.preprocessing.misc.Cropper(region=WAVENUMBER_RANGE)
    spectrum = cropper.apply(sample.spectrum)

    spectra_to_visualise.append(spectrum)

for sample in plate:
    print(sample)

title = "PLEASE PROVIDE TITLE"

rp.plot.spectra(
    spectra_to_visualise, label=sample_labels, plot_type="single", title=title
)

rp.plot.show()
