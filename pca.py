import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ramanspy as rp

import pathlib
import sys

from contextlib import redirect_stdout, redirect_stderr
from filter import (
    ROWS_TO_REMOVE,
    COLS_TO_REMOVE,
    MACBOOK_URL,
    ANALYSIS_FOLDER,
    OUTPUT_FOLDER,
    WAVENUMBER_RANGE,
    sort_files,
)
from matplotlib.ticker import MaxNLocator
from parse import parse
from pprint import pprint
from pyphi import pyphi as phi
from pyphi import pyphi_batch as pb
from pyphi import pyphi_plots as pp
from sample import Sample
from spectra import display_spectra

# Parse any multiwell files in the analyse/ folder
files, sample_labels = parse()

title = input("Data analysed: ").title()
print()

# Display the spectra
display_spectra(files, title)

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
            drug_loading=f"{sample.drug_loading} %",
            polymer=sample.polymer,
            polymer_loading=f"{sample.polymer_loading} %",
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

principle_components = int(input("Number of Principle Components: "))
print()

x = [x for x in range(1, principle_components + 1)]

with open(f"{OUTPUT_FOLDER}/diagnostics.txt", "w") as f:
    with redirect_stdout(f), redirect_stderr(f):
        pcaobj = phi.pca(spectral_df, principle_components)


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

if len(x) != len(y):
    raise ValueError("x and y must be the same length")

num_pcs = len(x)
filename = f"PC - sum(r2x)_{num_pcs} PCs.png"

# Plot PCs vs sum(R2X) as a line graph
fig, ax = plt.subplots()
ax.plot(x, y)

# Line + points in bold
ax.plot(
    x,
    y,
    marker="o",
    linestyle="-",
    linewidth=1.5,
    markersize=4,
    markeredgewidth=2,
)

ax.set_xlabel("Principal Components")
ax.set_ylabel("Sum(r2x)")
ax.set_title("Principal Components vs Sum(r2x)")

# Axis settings
ax.set_xlim(left=0)
ax.set_ylim(top=1)

# Whole numbers only on x-axis
ax.xaxis.set_major_locator(MaxNLocator(integer=True))


# Set window title (popup name)
fig.canvas.manager.set_window_title(filename)

fig.savefig(filename, bbox_inches="tight", dpi=300)
plt.show()


print(
    f"""PCA successfully conducted with {principle_components} Principle Components.\n
Please see \"{OUTPUT_FOLDER}/dataframes.txt\" for the dataframes analysed by PCA.\n
Please see \"{OUTPUT_FOLDER}/diagnostics.txt\" for the diagnostics sent to the terminal.\n
Please see \"{OUTPUT_FOLDER}/pcaobj.txt\" for the elements of the PCA model.
"""
)

options = []
for i in sample_df.columns:
    options.append(i)
options.append("none")

print(f"Options: {options}\n")
colorby = input("Colour plots by: ").lower()
print()

if colorby not in options:
    sys.exit("Column does not exist. Cannot colour by this parameter.")

first_PC = int(input("Number of first Principle Component: "))
print()

if first_PC < 1 or first_PC > principle_components:
    sys.exit(
        "Principle Component must be greater than or equal to 1 and less than total number of Principle Components."
    )

second_PC = int(input("Number of second Principle Component: "))
print()

if second_PC == first_PC:
    sys.exit("Second Principle Component cannot equal the first.")

if colorby == "none":
    TITLE = f"{title} with {principle_components} Principle Components"
    FILENAME = f"{title}_{principle_components} PCs_PC{first_PC} - PC{second_PC}"

    pp.score_scatter(
        pcaobj,
        [first_PC, second_PC],
        addtitle=TITLE,
        filename=FILENAME,
    )


else:
    TITLE = f"{title} coloured by {colorby.capitalize()} with {principle_components} Principle Components"
    FILENAME = f"{title}_{colorby.capitalize()}_{principle_components} PCs_PC{first_PC} - PC{second_PC}"

    pp.score_scatter(
        pcaobj,
        [first_PC, second_PC],
        addtitle=TITLE,
        CLASSID=sample_df,
        colorby=colorby,
        filename=FILENAME,
    )

pp.diagnostics(
    pcaobj,
    addtitle=TITLE,
    filename=FILENAME,
)
