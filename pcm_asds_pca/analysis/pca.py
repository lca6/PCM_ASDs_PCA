# ====================================================================================
# This script conducts PCA on the Raman spectra of the samples in the analyse/ folder.
# The settings for PCA are defined in settings.py
# The PCA model is saved to the pca_output/ folder.
# ====================================================================================

import json
import numpy as np
import pandas as pd
import pathlib
import pcm_asds_pca.pyphi.pyphi as phi
import ramanspy as rp
import shutil
import sys
import time

from contextlib import redirect_stderr, redirect_stdout

from pcm_asds_pca.config.settings import (
    COLS_TO_REMOVE,
    CONDUCT_PCA,
    CROSS_VAL,
    PATH_TO_DIR,
    NUM_PCS,
    PCA_OUTPUT,
    PLATES_TO_REMOVE,
    ROWS_TO_REMOVE,
    PREPROCESS_WITH_SAVGOL,
    PREPROCESS_WITH_SNV,
    SAVGOL_DERIVATIVE,
    SAVGOL_POLYNOMIAL,
    SAVGOL_WINDOW,
    WAVENUMBER_RANGE,
)

from pcm_asds_pca.core.parse import parse

from pcm_asds_pca.core.sample import Sample

from pprint import pprint


def main():

    # Define upper and lower bounds for wavenumber range to be included in PCA
    if WAVENUMBER_RANGE[0] is None:
        lower_bound = 0
    else:
        lower_bound = WAVENUMBER_RANGE[0]

    if WAVENUMBER_RANGE[1] is None:
        upper_bound = 2000
    else:
        upper_bound = WAVENUMBER_RANGE[1]

    # Check that PCA is set to be conducted
    if CONDUCT_PCA is False:
        sys.exit("CONDUCT_PCA is set to False in settings.py")

    # Moves files from pca_output to Bin
    folder = pathlib.Path(f"{PATH_TO_DIR}/{PCA_OUTPUT}")
    trash = pathlib.Path.home() / ".Trash"

    if folder.exists() and any(folder.iterdir()):

        print()
        delete = input(
            f"Delete all files from {PATH_TO_DIR}{PCA_OUTPUT}? (y/n) "
        ).lower()
        print()

        if delete == "n":
            sys.exit("PCA aborted")

        for item in folder.iterdir():
            if item.is_file() and delete == "y":
                shutil.move(str(item), trash / item.name)

        time.sleep(3)

    else:
        folder.mkdir(parents=True, exist_ok=True)

    # Parse all multiwell files in the analyse/ folder
    parsed_files = parse()

    dataframes_1_and_2 = []
    dataframe_3 = []
    dicts = []

    print("Creating dataframes...")
    print()

    for file in parsed_files:

        spectrum = rp.load.labspec(f"{PATH_TO_DIR}{file}")

        sample = Sample(file, spectrum)

        # ====================================
        # Filter samples to be included in PCA
        # ====================================

        if sample.row in ROWS_TO_REMOVE:
            continue
        elif sample.col in COLS_TO_REMOVE:
            continue
        elif sample.plate in PLATES_TO_REMOVE:
            continue
        elif sample.appearance == "":
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

        with open(f"{PATH_TO_DIR}{file}") as f:

            l_1_2 = []
            l_3 = []

            for line in f:
                if line[0] != "#":
                    shift, intensity = line.split("\t", maxsplit=1)

                    shift = float(shift)
                    intensity = float(intensity[:-1])

                    # Crop dataframe according to WAVENUMBER_RANGE
                    if lower_bound != 0:
                        if shift < lower_bound:
                            continue

                    if upper_bound != 2000:
                        if shift > upper_bound:
                            continue

                    if sample.plate in [0, 1, 2]:

                        l_1_2.append(
                            dict(
                                sample=sample,
                                shift=shift,
                                intensity=intensity,
                            )
                        )

                    elif sample.plate == 3:

                        l_3.append(
                            dict(
                                sample=sample,
                                shift=shift,
                                intensity=intensity,
                            )
                        )

            if l_1_2 != []:
                df = pd.DataFrame(l_1_2)
                df = df.pivot(index="sample", columns="shift", values="intensity")
                dataframes_1_and_2.append(df)

            if l_3 != []:
                df = pd.DataFrame(l_3)
                df = df.pivot(index="sample", columns="shift", values="intensity")
                dataframe_3.append(df)

    plates_1_and_2 = pd.concat(dataframes_1_and_2)

    # ========================================================================================================================================
    # NOTE: Plates 1 and 2 were collected with an acquisition time of 5s whereas plate 3 was collected with an acquisition time of 3s.
    # This means that the shift values for plate 3 are different to those of plates 1 and 2. Because plate 3's shifts only vary from plates
    # 1 and 2 by a maximum of 0.07 across the entire wavenumber range (please see check.py from an earlier commit), the decision was made to
    # combine plate 3's data into the dataframe for PCA using the shift numbers from plates 1 and 2. This means that the shift numbers for
    # plate 3 have been disregarded. To avoid this error, acquisition time should be consistent across plates when collecting using multiwell.
    # ========================================================================================================================================

    if dataframe_3 != []:

        plate_3 = pd.concat(dataframe_3)

        if plate_3.shape[1] != plates_1_and_2.shape[1]:
            sys.exit(
                "The dataframe for plate 3 does not have the same number of columns as the dataframe for plates 1 and 2."
            )

        plate_3_aligned = pd.DataFrame(
            plate_3.values,
            columns=plates_1_and_2.columns,
            index=plate_3.index,
        )

        spectral_df = pd.concat([plates_1_and_2, plate_3_aligned], axis=0)

    else:
        spectral_df = plates_1_and_2

    print(
        f"Dataframes created with shifts between {lower_bound} and {upper_bound} cm-1"
    )
    print()

    sample_df = pd.DataFrame(dicts).set_index("sample")

    # =============
    # Preprocessing
    # =============

    if PREPROCESS_WITH_SNV is True:
        print("Processing with Standard Normal Variate...")
        print()
        spectral_df = phi.spectra_snv(spectral_df)
        print("Standard Normal Variate applied.")
        print()

    if PREPROCESS_WITH_SAVGOL is True:
        print("Processing with Savitzky-Golay...")
        print()
        spectral_df, _ = phi.spectra_savgol(
            SAVGOL_WINDOW, SAVGOL_DERIVATIVE, SAVGOL_POLYNOMIAL, spectral_df
        )
        print(
            f"Savitzky-Golay filter applied with derivative order {SAVGOL_DERIVATIVE}, polynomial order {SAVGOL_POLYNOMIAL}, and window size {SAVGOL_WINDOW}."
        )
        print()

    # Save dataframes to .txt file
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

    # Save sample_df to .pkl file
    # This file is not human-readable
    sample_df.to_pickle(f"{PCA_OUTPUT}/sample_df_not_viewable.pkl")

    # Check that CROSS_VAL and NUM_PCS are set to valid values
    if CROSS_VAL > 100 or CROSS_VAL < 0:
        sys.exit("CROSS_VAL must be an integer between 0 and 100")

    if NUM_PCS <= 0:
        sys.exit("NUM_PCS must be an integer greater than 0")

    with open(f"{PCA_OUTPUT}/pca_terminal_output.txt", "w") as f:
        with redirect_stderr(f), redirect_stdout(f):

            # ============================
            # Principle Component Analysis
            # ============================

            pcaobj = phi.pca(spectral_df, int(NUM_PCS), cross_val=int(CROSS_VAL))

    # Save pcaobj to a .txt file
    with open(f"{PCA_OUTPUT}/pcaobj.txt", "w") as f:
        pprint(pcaobj, stream=f)

    # Save settings from settings.py at PCA runtime
    with open(f"{PCA_OUTPUT}/pca_settings.json", "w") as f:

        settings = {}
        settings["Principle Components"] = NUM_PCS
        settings["Cross_val"] = CROSS_VAL
        settings["Savitzky-Golay"] = PREPROCESS_WITH_SAVGOL

        if PREPROCESS_WITH_SAVGOL is True:
            settings["Savitzky-Golay Derivative"] = SAVGOL_DERIVATIVE
            settings["Savitzky-Golay Polynomial"] = SAVGOL_POLYNOMIAL
            settings["Savitzky-Golay Window"] = SAVGOL_WINDOW

        settings["Standard Normal Variate"] = PREPROCESS_WITH_SNV
        settings["Plates removed"] = PLATES_TO_REMOVE
        settings["Sample rows removed"] = ROWS_TO_REMOVE
        settings["Sample columns removed"] = COLS_TO_REMOVE
        settings["Wavenumber range"] = WAVENUMBER_RANGE

        json.dump(settings, f, indent=2)

    # Confirm PCA ran successfully
    for i in pcaobj["r2x"]:

        if np.isnan(i):
            sys.exit(f"PCA not successful.")

    # If successful, save pcaobj to .npy file
    # This is a format that can be loaded into Python for plotting and further analysis
    # This file is not human-readable
    np.save(f"{PCA_OUTPUT}/pcaobj_not_viewable.npy", pcaobj)

    sys.exit(
        f"""PCA successfully conducted with {NUM_PCS} Principle Components, removing {CROSS_VAL}% of data per round.\n
    Please see \"{PCA_OUTPUT}/dataframes.txt\" for the dataframes analysed by PCA.\n
    Please see \"{PCA_OUTPUT}/files_analysed.txt\" for a list of the files analysed.\n
    Please see \"{PCA_OUTPUT}/pca_settings.json\" for the settings applied to the dataframes before PCA.\n
    Please see \"{PCA_OUTPUT}/pca_terminal_output.txt\" for the diagnostics sent to the terminal.\n
    Please see \"{PCA_OUTPUT}/pcaobj.txt\" for the elements of the PCA model.
    """
    )


if __name__ == "__main__":
    main()
