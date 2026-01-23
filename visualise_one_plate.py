import ramanspy as rp

import sys
import pathlib
import re

from filter import rows_to_remove, cols_to_remove, macbook_url, processing_folder, wavenumber_range
from sample import Sample


# =======================
# Visualising the spectra
# ========================

files_to_be_processed = pathlib.Path(processing_folder)
files_to_be_processed = [str(x) for x in files_to_be_processed.iterdir()]

plate = []
spectra_to_visualise = []
spectra_labels = []


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
        spectra_labels.append(sample.well)


# Confirm samples have been provided
try:
    plate[0]
except IndexError:
    sys.exit("No files to be processed")


# Confirm all samples are from one plate
plate_nums = []
for sample in plate:
    plate_nums.append(sample.plate)

    for n in plate_nums:
        if sample.plate != n:
            sys.exit("Make sure all samples are from one plate")



if spectra_labels == ["N/A"]:
    spectra_labels[0] = "Glass reference"

# Won't sort the glass reference sample
else:
    spectra_labels.sort(
        key=lambda x: (re.findall(r"\D+", x)[0], int(re.findall(r"\d+", x)[0]))
    )

rp.plot.spectra(
    spectra_to_visualise,
    label=spectra_labels,
    plot_type="single",
    title=f"Plate #{plate[0].plate} Concentration {plate[0].concentration} mg/mL",
)

rp.plot.show()