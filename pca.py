import json
import numpy as np
import pandas as pd
import ramanspy as rp
import sys

from contextlib import redirect_stderr, redirect_stdout

from parse import parse
from pprint import pprint
from pyphi import pyphi as phi
from sample import Sample

from settings import (
    COLS_TO_REMOVE,
    CONDUCT_PCA,
    CROSS_VAL,
    MACBOOK_URL,
    NUM_PCS,
    PCA_OUTPUT,
    ROWS_TO_REMOVE,
    PREPROCESS_WITH_SAVGOL,
    PREPROCESS_WITH_SNV,
    SAVGOL_DERIVATIVE,
    SAVGOL_POLYNOMIAL,
    SAVGOL_WINDOW,
    WAVENUMBER_RANGE,
)


# Parse any multiwell files in the analyse/ folder
parsed_files, _ = parse()

# Save parsed_files to txt file
with open(f"{PCA_OUTPUT}/parsed_files.txt", "w") as f:
    json.dump(parsed_files, f)

dataframes_2_and_3 = []
dataframe_4 = []
dicts = []

for file in parsed_files:

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
            position=sample.position,
            appearance=sample.appearance,
        )
    )

    # =========================
    # Create spectral dataframe
    # =========================

    with open(f"{MACBOOK_URL}{file}") as f:

        l_2_3 = []
        l_4 = []

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

                if sample.plate in [2, 3]:

                    l_2_3.append(
                        dict(
                            sample=sample,
                            shift=shift,
                            intensity=intensity,
                        )
                    )

                elif sample.plate == 4:

                    l_4.append(
                        dict(
                            sample=sample,
                            shift=shift,
                            intensity=intensity,
                        )
                    )

        if l_2_3 != []:
            df = pd.DataFrame(l_2_3)
            df = df.pivot(index="sample", columns="shift", values="intensity")
            dataframes_2_and_3.append(df)

        if l_4 != []:
            df = pd.DataFrame(l_4)
            df = df.pivot(index="sample", columns="shift", values="intensity")
            dataframe_4.append(df)

plates_2_and_3 = pd.concat(dataframes_2_and_3)

# NOTE: Plates 2 and 3 were collected with an accumulation time of 5s whereas plate 4 was collected with an accumulation time of 3s.
# This means that the shift values for plate 4 are different to those of plates 2 and 3. Because plate 4's shifts only vary from plates
# 2 and 3 by a maximum of 0.07 across the entire wavenumber range (please run 'python check.py' to confirm), the decision was made to
# combine plate 4's data into the dataframe for PCA using the shift numbers from plates 2 and 3. This means that the shift numbers for
# plate 4 have been disregarded. To avoid this error, accumulation time should be consistent across plates.

if dataframe_4 != []:

    plate_4 = pd.concat(dataframe_4)

    if plate_4.shape[1] != plates_2_and_3.shape[1]:
        sys.exit(
            "The dataframe for plate 4 does not have the same number of columns as the dataframe for plates 2 and 3."
        )

    plate_4_aligned = pd.DataFrame(
        plate_4.values,
        columns=plates_2_and_3.columns,
        index=plate_4.index,
    )

    spectral_df = pd.concat([plates_2_and_3, plate_4_aligned], axis=0)

else:
    spectral_df = plates_2_and_3


# =============
# Preprocessing
# =============


if PREPROCESS_WITH_SAVGOL is True:

    spectral_df, _ = phi.spectra_savgol(
        SAVGOL_WINDOW, SAVGOL_DERIVATIVE, SAVGOL_POLYNOMIAL, spectral_df
    )
    print(
        f"Savitzky-Golay filter applied with derivative order {SAVGOL_DERIVATIVE}, polynomial order {SAVGOL_POLYNOMIAL}, and window size {SAVGOL_WINDOW}."
    )
    print()


if PREPROCESS_WITH_SNV is True:
    spectral_df = phi.spectra_snv(spectral_df)
    print("Standard Normal Variate applied.")
    print()


sample_df = pd.DataFrame(dicts).set_index("sample")

with open(f"{PCA_OUTPUT}/dataframes.txt", "w") as f:
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
        print(spectral_df, file=f)
        print(file=f)
        print(file=f)
        print(sample_df, file=f)

# Save spectral_df to txt file (binary format)
spectral_df.to_pickle(f"{PCA_OUTPUT}/spectral_df_not_viewable.pkl")

# Save sample_df to txt file (binary format)
sample_df.to_pickle(f"{PCA_OUTPUT}/sample_df_not_viewable.pkl")

if CONDUCT_PCA is True:

    if CROSS_VAL > 100 or CROSS_VAL < 0:
        sys.exit("CROSS_VAL must be an integer between 0 and 100")

    if NUM_PCS < 0:
        sys.exit("NUM_PCS must be an integer greater than 0")

    with open(f"{PCA_OUTPUT}/pca_terminal_output.txt", "w") as f:
        with redirect_stderr(f), redirect_stdout(f):

            # ============================
            # Principle Component Analysis
            # ============================

            pcaobj = phi.pca(spectral_df, int(NUM_PCS), cross_val=int(CROSS_VAL))

    with open(f"{PCA_OUTPUT}/pcaobj_{NUM_PCS} PCs_crossval{CROSS_VAL}.txt", "w") as f:
        print(f"Principle Components: {NUM_PCS} PCs", file=f)
        print(f"Cross_val: {CROSS_VAL}%", file=f)
        print(f"Savitzky-Golay: {PREPROCESS_WITH_SAVGOL}", file=f)
        print(f"Standard Normal Variate: {PREPROCESS_WITH_SNV}", file=f)
        pprint(pcaobj, stream=f)

    # Confirm PCA ran successfully
    for i in pcaobj["r2x"]:

        if np.isnan(i):
            sys.exit(f"PCA not successful.")

    # If successful, save pcaobj to npy file
    np.save(f"{PCA_OUTPUT}/pcaobj_not_viewable.npy", pcaobj)

    sys.exit(
        f"""PCA successfully conducted with {NUM_PCS} Principle Components, removing {CROSS_VAL}% of data per round.\n
    Please see \"{PCA_OUTPUT}/dataframes.txt\" for the dataframes analysed by PCA.\n
    Please see \"{PCA_OUTPUT}/diagnostics.txt\" for the diagnostics sent to the terminal.\n
    Please see \"{PCA_OUTPUT}/pcaobj.txt\" for the elements of the PCA model.
    """
    )
