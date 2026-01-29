import numpy as np
import pandas as pd
import ramanspy as rp
import sys

from contextlib import redirect_stderr, redirect_stdout

from parse import parse
from pprint import pprint
from pyphi import pyphi as phi
from pyphi import pyphi_plots as pp
from sample import Sample

from settings import (
    COLORBY,
    COLS_TO_REMOVE,
    CROSS_VAL,
    DISPLAY_DIAGNOSTICS,
    DISPLAY_PCs_R2X,
    DISPLAY_SCORE_SCATTER,
    DISPLAY_SPECTRA,
    FIRST_PC,
    MACBOOK_URL,
    NAME,
    NUM_PCS,
    OUTPUT_FOLDER,
    ROWS_TO_REMOVE,
    SAVGOL,
    SAVGOL_DERIVATIVE,
    SAVGOL_POLYNOMIAL,
    SAVGOL_WINDOW,
    SECOND_PC,
    WAVENUMBER_RANGE,
)

from spectra import display_PCs_R2X, display_spectra

# Parse any multiwell files in the analyse/ folder
files, sample_labels = parse()

if DISPLAY_SPECTRA is True:
    display_spectra(files, NAME)

dataframes = []
dicts = []

for file in files:

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
            concentration=f"{sample.concentration} mg/mL",
            drug=sample.drug,
            drug_loading=f"{sample.drug_loading}%",
            polymer=sample.polymer,
            polymer_loading=f"{sample.polymer_loading}%",
            position=sample.position,
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

# =============
# Preprocessing
# =============


if SAVGOL is True:
    spectral_df = phi.spectra_savgol(
        SAVGOL_WINDOW, SAVGOL_DERIVATIVE, SAVGOL_POLYNOMIAL, spectral_df
    )
    print("Savitzky-Golay filter applied")
    print()


sample_df = pd.DataFrame(dicts)

with open(f"{OUTPUT_FOLDER}/dataframes.txt", "w") as f:
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

x = [x for x in range(1, NUM_PCS + 1)]

if CROSS_VAL > 100 or CROSS_VAL < 0:
    sys.exit("cross_val must be an integer between 0 and 100")

with open(f"{OUTPUT_FOLDER}/diagnostics.txt", "w") as f:
    with redirect_stdout(f), redirect_stderr(f):
        pcaobj = phi.pca(spectral_df, NUM_PCS, cross_val=CROSS_VAL)


with open(f"{OUTPUT_FOLDER}/pcaobj.txt", "w") as f:
    with redirect_stdout(f), redirect_stderr(f):
        pprint(pcaobj)

    y = []
    sum_r2x = 0

    for i in pcaobj["r2x"]:

        if np.isnan(i):
            sys.exit(
                f'PCA not successful. Please check "{OUTPUT_FOLDER}/pcaobj.txt" for the elements of the PCA model.'
            )
        else:
            sum_r2x += i
            y.append(round(sum_r2x, 3))

if DISPLAY_PCs_R2X is True:
    display_PCs_R2X(x, y)

print(
    f"""PCA successfully conducted with {NUM_PCS} Principle Components.\n
Please see \"{OUTPUT_FOLDER}/dataframes.txt\" for the dataframes analysed by PCA.\n
Please see \"{OUTPUT_FOLDER}/diagnostics.txt\" for the diagnostics sent to the terminal.\n
Please see \"{OUTPUT_FOLDER}/pcaobj.txt\" for the elements of the PCA model.
"""
)

options = []
for i in sample_df.columns:
    options.append(i)
options.append("none")

if COLORBY.lower() not in options:
    sys.exit(f"Column does not exist. Cannot colour by this parameter. Options: {options}\n")

if FIRST_PC < 1 or FIRST_PC > NUM_PCS:
    sys.exit(
        "Principle Component must be greater than or equal to 1 and less than total number of Principle Components."
    )

if SECOND_PC == FIRST_PC:
    sys.exit("Second Principle Component cannot equal the first.")

if COLORBY == "none":
    TITLE = f"{NAME} with {NUM_PCS} Principle Components"
    FILENAME = f"{NAME}_{NUM_PCS} PCs_PC{FIRST_PC} - PC{SECOND_PC}"
else:
    TITLE = f"{NAME} coloured by {COLORBY.capitalize()} with {NUM_PCS} Principle Components"
    FILENAME = (
        f"{NAME}_{COLORBY.capitalize()}_{NUM_PCS} PCs_PC{FIRST_PC} - PC{SECOND_PC}"
    )


if DISPLAY_SCORE_SCATTER is True:
    if COLORBY == "none":
        pp.score_scatter(
            pcaobj,
            [FIRST_PC, SECOND_PC],
            addtitle=TITLE,
            filename=FILENAME,
        )

    else:
        pp.score_scatter(
            pcaobj,
            [FIRST_PC, SECOND_PC],
            addtitle=TITLE,
            CLASSID=sample_df,
            colorby=COLORBY,
            filename=FILENAME,
        )

if DISPLAY_DIAGNOSTICS is True:
    pp.diagnostics(
        pcaobj, addtitle=TITLE, filename=FILENAME, score_plot_xydim=[FIRST_PC, SECOND_PC]
    )

