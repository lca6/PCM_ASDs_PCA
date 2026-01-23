import ramanspy as rp

import sys
import pathlib
import re

from filter import (
    rows_to_remove,
    cols_to_remove,
    macbook_url,
    processing_folder,
    wavenumber_range,
    sort_files,
)
from sample import Sample


# =======================
# Visualising the spectra
# ========================

files = pathlib.Path(processing_folder)
files = [str(x) for x in files.iterdir()]

# Confirm samples have been provided
try:
    files[0]
except IndexError:
    sys.exit("No files provided")

files_to_be_processed, sample_labels = sort_files(files)

plate = []
spectra_to_visualise = []

for file in files_to_be_processed:

    with open(file, encoding="latin-1") as f:
        text = f.read()

    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

    # Loads the Raman object for visualising the spectrum
    spectrum = rp.load.labspec(f"{macbook_url}{file}")

    sample = Sample()

    sample.get_sample_metadata(file, spectrum)

    plate.append(sample)

    # Filter spectra to be visualised
    if sample.row in rows_to_remove:
        continue
    elif sample.col in cols_to_remove:
        continue

    # =============
    # Preprocessing
    # =============

    # Crop spectra
    cropper = rp.preprocessing.misc.Cropper(region=wavenumber_range)
    spectrum = cropper.apply(sample.spectrum)

    spectra_to_visualise.append(spectrum)

for sample in plate:
    print(sample)

rp.plot.spectra(
    spectra_to_visualise,
    label=sample_labels,
    plot_type="single",
)

rp.plot.show()
