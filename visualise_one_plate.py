import ramanspy as rp

import sys
import os
import pathlib
import re

from dotenv import load_dotenv
from sample import Sample

load_dotenv()

macbook_url = os.getenv("MACBOOK_URL")


# =======================
# Visualising the spectra
# ========================

files_to_be_processed = pathlib.Path("to_be_processed")
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

        sample = Sample(spectrum)

        sample.extract_metadata(file)

        plate.append(sample)

        spectra_to_visualise.append(sample.spectrum)

        spectra_labels.append(sample.position)



# Confirm all samples are from one plate
plate_num = []
for sample in plate:
    plate_num.append(sample.plate)

    for n in plate_num:
        if sample.plate != n:
            sys.exit("Make sure all samples are from one plate")


# Confirm samples have been provided
try:
    plate[0]
except IndexError:
    sys.exit("No files to be processed")


if spectra_labels == ["N/A"]:
    spectra_labels[0] = "Glass reference"
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