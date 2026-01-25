import pandas as pd
import numpy as np
import ramanspy as rp

import sys
import pathlib

from filter import (
    ROWS_TO_REMOVE,
    COLS_TO_REMOVE,
    MACBOOK_URL,
    ANALYSIS_FOLDER,
    WAVENUMBER_RANGE,
    sort_files,
)
from sample import Sample
from pyphi import pyphi as phi
from pyphi import pyphi_plots as pp
from pyphi import pyphi_batch as pb


files = pathlib.Path(ANALYSIS_FOLDER)
files = [str(x) for x in files.iterdir()]

plate = []
dataframes = []

# Confirm samples have been provided
try:
    files[0]
except IndexError:
    sys.exit("No files provided")


files, sample_labels = sort_files(files)


for file in files:

    with open(file, encoding="latin-1") as f:
        text = f.read()

    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

    spectrum = rp.load.labspec(f"{MACBOOK_URL}{file}")

    sample = Sample()

    sample.get_sample_metadata(file, spectrum)

    plate.append(sample)

    # =============
    # Preprocessing
    # =============

    # Filter samples to be included in PCA
    if sample.row in ROWS_TO_REMOVE:
        continue
    elif sample.col in COLS_TO_REMOVE:
        continue

    with open(f"{MACBOOK_URL}{file}") as f:

        file = []
        for line in f:
            if line[0] != "#":
                shift, intensity = line.split("\t", maxsplit=1)

                shift = float(shift)
                intensity = float(intensity[:-1])

                # Crop dataframe according to WAVENUMBER_RANGE
                if WAVENUMBER_RANGE[0] is not None:
                    if shift < WAVENUMBER_RANGE[0]:
                        continue

                if WAVENUMBER_RANGE[1] is not None:
                    if shift > WAVENUMBER_RANGE[1]:
                        continue

                file.append(
                    dict(
                        sample=sample.well,
                        shift=shift,
                        intensity=intensity,
                    )
                )

        df = pd.DataFrame(file)

        df = df.pivot(index="sample", columns="shift", values="intensity")

        dataframes.append(df)



# ============================
# Principle Component Analysis
# ============================

spectral_data = pd.concat(dataframes)

print(spectral_data)

pcaobj = phi.pca(spectral_data, 3)

# ========================================================
# Plotting scores and loadings of each Principle Component
# ========================================================

title = "PLEASE PROVIDE TITLE"

pp.score_scatter(pcaobj, [1, 2], addtitle=title)

