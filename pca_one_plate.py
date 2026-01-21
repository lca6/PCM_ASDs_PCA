import pandas as pd
import numpy as np
import pyphi as phi
import pyphi_plots as pp
import ramanspy as rp

import dotenv
import sys
import os
import pathlib

from sample import Sample

dotenv.load_dotenv()

macbook_url = os.getenv("MACBOOK_URL")
processing_folder = os.getenv("PROCESSING_FOLDER")

files_to_be_processed = pathlib.Path(processing_folder)
files_to_be_processed = [str(x) for x in files_to_be_processed.iterdir()]

plate = []
dataframes = []

for file in files_to_be_processed:

    with open(file, encoding="latin-1") as f:
        text = f.read()

    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

    spectrum = rp.load.labspec(f"{macbook_url}{file}")

    sample = Sample()

    sample.get_sample_metadata(file, spectrum)

    plate.append(sample)


    with open(f"{macbook_url}{file}") as f:

        file = []
        for line in f:
            if line[0] != "#":
                shift, intensity = line.split("\t", maxsplit=1)
                file.append(
                    dict(
                        sample=sample.well,
                        shift=shift,
                        intensity=intensity[:-1],
                    )
                )

        file = pd.DataFrame(file)

        # Convert data to floats before pivoting
        file["shift"] = file["shift"].astype(float)
        file["intensity"] = file["intensity"].astype(float)

        file = file.pivot(index="sample", columns="shift", values="intensity")

        dataframes.append(file)



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



# ============
# Preprocessing
# =============
# TODO

# ============================
# Principle Component Analysis
# ============================

spectral_data = pd.concat(dataframes)

print(spectral_data)

pcaobj = phi.pca(spectral_data, 3)
