import pandas as pd
import numpy as np
import ramanspy as rp

import sys
import pathlib

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
from pyphi import pyphi as phi
from pyphi import pyphi_plots as pp
from pyphi import pyphi_batch as pb


files = pathlib.Path(ANALYSIS_FOLDER)
files = [str(x) for x in files.iterdir()]


# Confirm samples have been provided
try:
    files[0]
except IndexError:
    sys.exit("No files provided")


files, sample_labels = sort_files(files)

dataframes = []
dicts = []

for file in files:

    with open(file, encoding="latin-1") as f:
        text = f.read()

    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

    spectrum = rp.load.labspec(f"{MACBOOK_URL}{file}")

    sample = Sample(file, spectrum)

    # Filter samples to be included in PCA
    if sample.row in ROWS_TO_REMOVE:
        continue
    elif sample.col in COLS_TO_REMOVE:
        continue

    # =======================
    # Create sample dataframe
    # =======================

    dicts.append(
        dict(
            sample=sample,
            plate=sample.plate,
            well=sample.well,
            row=sample.row,
            column=sample.col,
            concentration=sample.concentration,
            drug=sample.drug,
            drug_loading=sample.drug_loading,
            polymer=sample.polymer,
            polymer_loading=sample.polymer_loading,
        )
    )

    # =========================
    # Create spectral dataframe
    # =========================

    with open(f"{MACBOOK_URL}{file}") as f:

        l = []
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

                l.append(
                    dict(
                        sample=sample,
                        shift=shift,
                        intensity=intensity,
                    )
                )

        df = pd.DataFrame(l)
        df = df.pivot(index="sample", columns="shift", values="intensity")
        dataframes.append(df)


spectral_df = pd.concat(dataframes)

sample_df = pd.DataFrame(dicts)

with open("dataframes.txt", "w") as f:
    with redirect_stdout(f), redirect_stderr(f):
        with pd.option_context(
            "display.max_rows",
            None,
            "display.max_columns",
            None,
            "display.max_colwidth",
            None,
            "display.width",
            None,
        ):
            print(spectral_df, "\n\n", sample_df)


# ============================
# Principle Component Analysis
# ============================

with open("diagnostics.txt", "w") as f:
    with redirect_stdout(f), redirect_stderr(f):
        pcaobj = phi.pca(spectral_df, 3)


with open("pcaobj.txt", "w") as f:
    with redirect_stdout(f), redirect_stderr(f):
        print(pcaobj)


print(
    """PCA successfully conducted.
Please see \"dataframes.txt\" for the dataframes analysed by PCA.
Please see \"diagnostics.txt\" for the diagnostics sent to the terminal.
Please see \"pcaobj.txt\" for the elements of the PCA model.
"""
)

title = input("Title for score scatter plot: ")
print(f"Options: {sample_df.columns}")
colorby = input("Color score scatter plot by: ")

pp.score_scatter(
    pcaobj, [1, 2], addtitle=title, CLASSID=sample_df, colorby=colorby, filename=title
)
