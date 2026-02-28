# ==================================================
# Spectra visualisation and plotting of PCA results.
# ==================================================

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pathlib
import pcm_asds_pca.pyphi.pyphi_plots as pp
import ramanspy as rp
import shutil
import sys
import time

from matplotlib.ticker import MaxNLocator

from pcm_asds_pca.config.settings import *

from pcm_asds_pca.core.sample import Sample


def main():

    # Read pcaobj from .npy file
    pcaobj = np.load(f"{PCA_OUTPUT}/pcaobj_not_viewable.npy", allow_pickle=True).item()

    # Filter pcaobj according to settings.py
    pcaobj, rows_to_remove = filter_pcaobj(pcaobj)

    # Read sample_df from .pkl file
    sample_df = pd.read_pickle(f"{PCA_OUTPUT}/sample_df_not_viewable.pkl")

    labels_to_remove = sample_df.index[rows_to_remove]

    # Filter sample_df to remove the same samples that were removed from pcaobj
    sample_df.drop(labels_to_remove, inplace=True)

    # Read num_pcs from pca_settings.json file
    with open(f"{PCA_OUTPUT}/pca_settings.json") as f:
        settings = json.load(f)
        num_pcs = settings["Principal Components"]

    # Create spectra_output folder if it doesn't exist
    folder = pathlib.Path(f"{SPECTRA_OUTPUT}")
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)

    # ===========
    # All samples
    # ===========

    # Filter sample_df by PLATES_TO_REMOVE_IN_SPECTRA, ROWS_TO_REMOVE_IN_SPECTRA and COLS_TO_REMOVE_IN_SPECTRA
    sample_df = sample_df[
        (~sample_df["plate"].isin(PLATES_TO_REMOVE_IN_SPECTRA)) &
        (~sample_df["row"].isin(ROWS_TO_REMOVE_IN_SPECTRA)) &
        (~sample_df["column"].isin(COLS_TO_REMOVE_IN_SPECTRA))
    ]

    sample_df_labels = (
        sample_df["well"]
        + " ("
        + sample_df["concentration"].astype(str)
        + " mg/mL)"
    ).tolist()

    # ========
    # Subset A
    # ========

    subset_A = [pos - 1 for pos in SUBSET_A_LIST]

    subset_A = sample_df.iloc[subset_A]

    # Create a list of sample labels
    # The label for each sample is in the format: "well (concentration mg/mL) (polymer)"
    subset_A_sample_labels = (
        subset_A["well"]
        + " ("
        + subset_A["concentration"].astype(str)
        + " mg/mL)"
        + " ("
        + subset_A["polymer"]
        + ")"
    ).tolist()

    # ========
    # Subset B
    # ========

    subset_B = [pos - 1 for pos in SUBSET_B_LIST]

    subset_B = sample_df.iloc[subset_B]

    subset_B_sample_labels = (
        subset_B["well"]
        + " ("
        + subset_B["concentration"].astype(str)
        + " mg/mL)"
        + " ("
        + subset_B["polymer"]
        + ")"
    ).tolist()

    # ========
    # Subset C
    # ========

    subset_C = [pos - 1 for pos in SUBSET_C_LIST]

    subset_C = sample_df.iloc[subset_C]

    subset_C_sample_labels = (
        subset_C["well"]
        + " ("
        + subset_C["concentration"].astype(str)
        + " mg/mL)"
        + " ("
        + subset_C["polymer"]
        + ")"
    ).tolist()

    # ========
    # Subset D
    # ========

    subset_D = [pos - 1 for pos in SUBSET_D_LIST]

    subset_D = sample_df.iloc[subset_D]

    subset_D_sample_labels = (
        subset_D["well"]
    ).tolist()

    # Save samples to spectra_samples.txt
    with open(f"{SPECTRA_OUTPUT}/{NAME}_spectra_samples.txt", "w") as f:

        print("Subset A", file=f)
        print(file=f)
        
        for s in subset_A_sample_labels:
            print(s, file=f)

        print(file=f)

        print("Subset B", file=f)
        print(file=f)

        for s in subset_B_sample_labels:
            print(s, file=f)
        
        print(file=f)

        print("Subset C", file=f)
        print(file=f)

        for s in subset_C_sample_labels:
            print(s, file=f)
        
        print(file=f)

        print("Subset D", file=f)
        print(file=f)

        for s in subset_D_sample_labels:
            print(s, file=f)
        
        print(file=f)

        print("All samples", file=f)
        print(file=f)

        for s in sample_df_labels:
            print(s, file=f)

    print()
    print(
        f'Please see "{SPECTRA_OUTPUT}/{NAME}_spectra_samples.txt" for a list of the samples displayed.'
    )
    print()

    # ===============================================
    # Pass subset_A and subset_B into display_spectra
    # ===============================================

    subsets = [subset_A, subset_B, subset_C, subset_D]

    subset_labels = [subset_A_sample_labels, subset_B_sample_labels, subset_C_sample_labels, subset_D_sample_labels]

    # ===============================================================================================
    # Display Raman spectra
    # The spectra are preprocessed with the same preprocessing techniques as those applied before PCA
    # This ensures that the spectra visualised are the same as those used for PCA
    # ===============================================================================================
    if DISPLAY_SPECTRA is True:

        if all(subset.empty for subset in subsets):
            display_spectra(samples=sample_df, labels=sample_df_labels, title=NAME)
        else:
            display_spectra_highlighted_by_subset(subsets=subsets, subset_labels=subset_labels, title=NAME)

    # ===========================================================================
    # Display a plot of the number of Principal Components (PCs) against sum(R2X)
    # This helps decide how many PCs to retain for analysis and visualisation
    # ===========================================================================
    if DISPLAY_PCs_R2X is True:

        display_PCs_R2X(num_pcs, pcaobj)

    # ==================================================================================
    # Display score scatter plot of FIRST_PC against SECOND_PC as defined in settings.py
    # Coloured by a parameter of choice (e.g. "concentration")
    # ==================================================================================
    if DISPLAY_SCORE_SCATTER is True:

        # Check that COLORBY, FIRST_PC and SECOND_PC are set to valid values
        options = []
        for i in sample_df.columns:
            options.append(i)
        options.append("none")

        colorby = COLORBY.lower()

        if colorby not in options:
            sys.exit(
                f"Column does not exist. Cannot colour by this parameter. Options: {options}\n"
            )

        if FIRST_PC < 1 or FIRST_PC > num_pcs:
            sys.exit(
                "First Principal Component must be greater than or equal to 1 and less than or equal to the total number of Principal Components."
            )

        if SECOND_PC < 1 or SECOND_PC > num_pcs:
            sys.exit(
                "Second Principal Component must be greater than or equal to 1 and less than or equal to the total number of Principal Components."
            )

        if SECOND_PC == FIRST_PC:
            sys.exit("Second Principal Component cannot equal the first.")

        # Set title and filename for score scatter plots based on NAME, COLORBY, FIRST_PC and SECOND_PC
        if colorby == "none":
            title = f"{NAME}"
            filename = f"{NAME}_{num_pcs} PCs_PC{FIRST_PC} - PC{SECOND_PC}"
        else:
            title = f"{NAME} coloured by {colorby.replace('_', ' ')}"
            filename = f"{NAME}_{colorby.capitalize()}_{num_pcs} PCs_PC{FIRST_PC} - PC{SECOND_PC}"

        first_pc_variance = round(pcaobj["r2x"][FIRST_PC - 1] * 100, 1)
        second_pc_variance = round(pcaobj["r2x"][SECOND_PC - 1] * 100, 1)

        # ========================================================
        # Display score scatter plot of FIRST_PC against SECOND_PC
        # ========================================================
        if colorby == "none":
            pp.score_scatter(
                pcaobj,
                [FIRST_PC, SECOND_PC],
                title=title,
                filename=filename,
                first_pc_variance=first_pc_variance,
                second_pc_variance=second_pc_variance,
                subset_A=SUBSET_A_LIST,
                subset_B=SUBSET_B_LIST,
                subset_C=SUBSET_C_LIST,
                subset_D=SUBSET_D_LIST,
            )

        else:
            pp.score_scatter(
                pcaobj,
                [FIRST_PC, SECOND_PC],
                title=title,
                CLASSID=sample_df,
                colorby=colorby,
                filename=filename,
                first_pc_variance=first_pc_variance,
                second_pc_variance=second_pc_variance,
                subset_A=SUBSET_A_LIST,
                subset_B=SUBSET_B_LIST,
                subset_C=SUBSET_C_LIST,
                subset_D=SUBSET_D_LIST,
            )

        # Wait for plots to load in browser
        time.sleep(5)

        # Move .html files to spectra_output/ folder
        src_dir = pathlib.Path(".")
        dst_dir = pathlib.Path(f"{SPECTRA_OUTPUT}")
        dst_dir.mkdir(parents=True, exist_ok=True)

        for html_file in src_dir.glob("*.html"):
            shutil.move(html_file, dst_dir / html_file.name)

    # ==============================
    # Display Hotelling's T2 and SPE
    # ==============================
    if DISPLAY_DIAGNOSTICS is True:

        try:
            pp.diagnostics(
                pcaobj,
                score_plot_xydim=[FIRST_PC, SECOND_PC],
                addtitle=NAME,
            )
        except np.linalg.LinAlgError:
            sys.exit(
                "Error in displaying diagnostics. Check the values of FIRST_PC and SECOND_PC in settings.py"
            )

        # Wait for plots to load in browser
        time.sleep(5)

        # Move .html files to spectra_output/ folder
        src_dir = pathlib.Path(".")
        dst_dir = pathlib.Path(f"{SPECTRA_OUTPUT}")
        dst_dir.mkdir(parents=True, exist_ok=True)

        for html_file in src_dir.glob("*.html"):
            shutil.move(html_file, dst_dir / html_file.name)


# ========================
# Visualising the spectra
# ========================
def display_spectra(samples, labels, title):

    title = title.capitalize()

    filename = f"raman_spectrum_{title}"

    if DISPLAY_SAMPLE_LABELS is False:
        labels = None

    pipeline = []

    # Extract preprocessing techniques conducted before PCA
    with open(f"{PCA_OUTPUT}/pca_settings.json") as f:
        settings = json.load(f)
        preprocess_with_savgol = settings["Savitzky-Golay"]
        preprocess_with_snv = settings["Standard Normal Variate"]

    if preprocess_with_snv is True:
        pipeline.append(rp.preprocessing.PreprocessingStep(standard_normal_variate))
        title += " + SNV"
        filename += "_snv"

    if preprocess_with_savgol is True:

        with open(f"{PCA_OUTPUT}/pca_settings.json") as f:
            settings = json.load(f)
            savgol_window = settings["Savitzky-Golay Window"]
            savgol_polynomial = settings["Savitzky-Golay Polynomial"]
            savgol_derivative = settings["Savitzky-Golay Derivative"]

        pipeline.append(
            rp.preprocessing.denoise.SavGol(
                window_length=savgol_window,
                polyorder=savgol_polynomial,
                deriv=savgol_derivative,
            )
        )
        title += f" + SG (Derivative {savgol_derivative}, Polynomial {savgol_polynomial}, Window size {savgol_window})"
        filename += f"_sg_deriv{savgol_derivative}_poly{savgol_polynomial}_win{savgol_window}"

    if pipeline == []:
        title += " (raw)"
        filename += "_raw"

    preprocessing_pipeline = rp.preprocessing.Pipeline(pipeline)

    # Read Wavenumber range from pca_settings.json file
    with open(f"{PCA_OUTPUT}/pca_settings.json") as f:
        settings = json.load(f)
        wavenumber_range = settings["Wavenumber range"]

    # Adjust wavenumber range for visualisation if necessary to ensure it is the same as or a subset of the wavenumber range used for PCA
    if wavenumber_range[0] is None:
        lower_bound_in_pca = MINIMUM_WAVENUMBER
    else:
        lower_bound_in_pca = wavenumber_range[0]

    if wavenumber_range[1] is None:
        upper_bound_in_pca = MAXIMUM_WAVENUMBER
    else:
        upper_bound_in_pca = wavenumber_range[1]

    if WAVENUMBER_RANGE_FOR_SPECTRA[0] is None:
        lower_bound_in_spectra = MINIMUM_WAVENUMBER
    else:
        lower_bound_in_spectra = WAVENUMBER_RANGE_FOR_SPECTRA[0]
    
    if WAVENUMBER_RANGE_FOR_SPECTRA[1] is None:
        upper_bound_in_spectra = MAXIMUM_WAVENUMBER
    else:
        upper_bound_in_spectra = WAVENUMBER_RANGE_FOR_SPECTRA[1]

    if lower_bound_in_spectra > lower_bound_in_pca:
        wavenumber_range[0] = lower_bound_in_spectra
    else:
        wavenumber_range[0] = lower_bound_in_pca

    if upper_bound_in_spectra < upper_bound_in_pca:
        wavenumber_range[1] = upper_bound_in_spectra
    else:
        wavenumber_range[1] = upper_bound_in_pca

    title += f" ({wavenumber_range[0]}-{wavenumber_range[1]} cm-1)"
    filename += f"_{wavenumber_range[0]}-{wavenumber_range[1]}cm-1"

    cropper = rp.preprocessing.misc.Cropper(region=wavenumber_range)

    spectra_to_visualise = []

    samples = samples.index.tolist()

    for sample in samples:

        # Filter spectra
        if sample.plate in PLATES_TO_REMOVE_IN_SPECTRA:
            continue
        elif sample.row in ROWS_TO_REMOVE_IN_SPECTRA:
            continue
        elif sample.col in COLS_TO_REMOVE_IN_SPECTRA:
            continue

        # Crop spectra
        spectrum = cropper.apply(sample.spectrum)

        # Preprocess the spectrum with the same preprocessing techniques as those applied before PCA
        preprocessed_spectrum = preprocessing_pipeline.apply(spectrum)

        spectra_to_visualise.append(preprocessed_spectrum)

    fig, ax = plt.subplots()

    # Plot the spectra overlaid on a single axis
    rp.plot.spectra(
        spectra_to_visualise,
        label=labels,
        plot_type="single",
        title=title,
        ax=ax,
        ylabel=SPECTRA_Y_AXIS_LABEL,
    )

    plt.savefig(f"{SPECTRA_OUTPUT}/{filename}", bbox_inches="tight", dpi=300)
    plt.show()


def display_spectra_highlighted_by_subset(subsets, subset_labels, title):

    title = title.capitalize()

    filename = f"raman_spectrum_{title}"

    subset_A = subsets[0].index.tolist()
    subset_B = subsets[1].index.tolist()
    subset_C = subsets[2].index.tolist()
    subset_D = subsets[3].index.tolist()

    if DISPLAY_SAMPLE_LABELS is True:
        subset_A_sample_labels = subset_labels[0]
        subset_B_sample_labels = subset_labels[1]
        subset_C_sample_labels = subset_labels[2]
        subset_D_sample_labels = subset_labels[3]
    else:
        subset_A_sample_labels = None
        subset_B_sample_labels = None
        subset_C_sample_labels = None
        subset_D_sample_labels = None

    pipeline = []

    # Extract preprocessing techniques conducted before PCA
    with open(f"{PCA_OUTPUT}/pca_settings.json") as f:
        settings = json.load(f)
        preprocess_with_savgol = settings["Savitzky-Golay"]
        preprocess_with_snv = settings["Standard Normal Variate"]

    if preprocess_with_snv is True:
        pipeline.append(rp.preprocessing.PreprocessingStep(standard_normal_variate))
        title += " + SNV"
        filename += "_snv"

    if preprocess_with_savgol is True:

        with open(f"{PCA_OUTPUT}/pca_settings.json") as f:
            settings = json.load(f)
            savgol_window = settings["Savitzky-Golay Window"]
            savgol_polynomial = settings["Savitzky-Golay Polynomial"]
            savgol_derivative = settings["Savitzky-Golay Derivative"]

        pipeline.append(
            rp.preprocessing.denoise.SavGol(
                window_length=savgol_window,
                polyorder=savgol_polynomial,
                deriv=savgol_derivative,
            )
        )
        title += f" + SG (Derivative {savgol_derivative}, Polynomial {savgol_polynomial}, Window size {savgol_window})"
        filename += f"_sg_deriv{savgol_derivative}_poly{savgol_polynomial}_win{savgol_window}"

    if pipeline == []:
        title += " (raw)"
        filename += "_raw"

    preprocessing_pipeline = rp.preprocessing.Pipeline(pipeline)

    # Read Wavenumber range from pca_settings.json file
    with open(f"{PCA_OUTPUT}/pca_settings.json") as f:
        settings = json.load(f)
        wavenumber_range = settings["Wavenumber range"]

    # Adjust wavenumber range for visualisation if necessary to ensure it is the same as or a subset of the wavenumber range used for PCA
    if wavenumber_range[0] is None:
        lower_bound_in_pca = MINIMUM_WAVENUMBER
    else:
        lower_bound_in_pca = wavenumber_range[0]

    if wavenumber_range[1] is None:
        upper_bound_in_pca = MAXIMUM_WAVENUMBER
    else:
        upper_bound_in_pca = wavenumber_range[1]

    if WAVENUMBER_RANGE_FOR_SPECTRA[0] is None:
        lower_bound_in_spectra = MINIMUM_WAVENUMBER
    else:
        lower_bound_in_spectra = WAVENUMBER_RANGE_FOR_SPECTRA[0]
    
    if WAVENUMBER_RANGE_FOR_SPECTRA[1] is None:
        upper_bound_in_spectra = MAXIMUM_WAVENUMBER
    else:
        upper_bound_in_spectra = WAVENUMBER_RANGE_FOR_SPECTRA[1]

    if lower_bound_in_spectra > lower_bound_in_pca:
        wavenumber_range[0] = lower_bound_in_spectra
    else:
        wavenumber_range[0] = lower_bound_in_pca

    if upper_bound_in_spectra < upper_bound_in_pca:
        wavenumber_range[1] = upper_bound_in_spectra
    else:
        wavenumber_range[1] = upper_bound_in_pca

    title += f" ({wavenumber_range[0]}-{wavenumber_range[1]} cm-1)"
    filename += f"_{wavenumber_range[0]}-{wavenumber_range[1]}cm-1"

    cropper = rp.preprocessing.misc.Cropper(region=wavenumber_range)

    subset_A_spectra = []

    for sample in subset_A:

        # Filter spectra
        if sample.plate in PLATES_TO_REMOVE_IN_SPECTRA:
            continue
        elif sample.row in ROWS_TO_REMOVE_IN_SPECTRA:
            continue
        elif sample.col in COLS_TO_REMOVE_IN_SPECTRA:
            continue

        # Crop spectra
        spectrum = cropper.apply(sample.spectrum)

        # Preprocess the spectrum with the same preprocessing techniques as those applied before PCA
        preprocessed_spectrum = preprocessing_pipeline.apply(spectrum)

        subset_A_spectra.append(preprocessed_spectrum)

    subset_B_spectra = []

    for sample in subset_B:

        # Filter spectra
        if sample.plate in PLATES_TO_REMOVE_IN_SPECTRA:
            continue
        elif sample.row in ROWS_TO_REMOVE_IN_SPECTRA:
            continue
        elif sample.col in COLS_TO_REMOVE_IN_SPECTRA:
            continue

        # Crop spectra
        spectrum = cropper.apply(sample.spectrum)

        # Preprocess the spectrum with the same preprocessing techniques as those applied before PCA
        preprocessed_spectrum = preprocessing_pipeline.apply(spectrum)

        subset_B_spectra.append(preprocessed_spectrum)

    subset_C_spectra = []

    for sample in subset_C:

        # Filter spectra
        if sample.plate in PLATES_TO_REMOVE_IN_SPECTRA:
            continue
        elif sample.row in ROWS_TO_REMOVE_IN_SPECTRA:
            continue
        elif sample.col in COLS_TO_REMOVE_IN_SPECTRA:
            continue

        # Crop spectra
        spectrum = cropper.apply(sample.spectrum)

        # Preprocess the spectrum with the same preprocessing techniques as those applied before PCA
        preprocessed_spectrum = preprocessing_pipeline.apply(spectrum)

        subset_C_spectra.append(preprocessed_spectrum)

    subset_D_spectra = []

    for sample in subset_D:

        # Filter spectra
        if sample.plate in PLATES_TO_REMOVE_IN_SPECTRA:
            continue
        elif sample.row in ROWS_TO_REMOVE_IN_SPECTRA:
            continue
        elif sample.col in COLS_TO_REMOVE_IN_SPECTRA:
            continue

        # Crop spectra
        spectrum = cropper.apply(sample.spectrum)

        # Preprocess the spectrum with the same preprocessing techniques as those applied before PCA
        preprocessed_spectrum = preprocessing_pipeline.apply(spectrum)

        subset_D_spectra.append(preprocessed_spectrum)

    fig, ax = plt.subplots()

    # Plot the spectra overlaid on a single axis
    rp.plot.spectra(
        subset_A_spectra,
        label=subset_A_sample_labels,
        plot_type="single",
        title=title,
        ax=ax,
        ylabel=SPECTRA_Y_AXIS_LABEL,
        color=HIGHLIGHTING_COLOURS[0],
    )

    rp.plot.spectra(
        subset_B_spectra,
        label=subset_B_sample_labels,
        plot_type="single",
        title=title,
        ax=ax,
        ylabel=SPECTRA_Y_AXIS_LABEL,
        color=HIGHLIGHTING_COLOURS[1],
    )

    rp.plot.spectra(
        subset_C_spectra,
        label=subset_C_sample_labels,
        plot_type="single",
        title=title,
        ax=ax,
        ylabel=SPECTRA_Y_AXIS_LABEL,
        color=HIGHLIGHTING_COLOURS[2],
    )

    rp.plot.spectra(
        subset_D_spectra,
        label=subset_D_sample_labels,
        plot_type="single",
        title=title,
        ax=ax,
        ylabel=SPECTRA_Y_AXIS_LABEL,
        color=HIGHLIGHTING_COLOURS[3],
    )

    plt.savefig(f"{SPECTRA_OUTPUT}/{filename}", bbox_inches="tight", dpi=300)
    plt.show()


# ===================================
# Plot number of PCs against sum(R2X)
# ===================================
def display_PCs_R2X(num_pcs, pcaobj):

    x_axis = [x for x in range(1, num_pcs + 1)]

    y_axis = []
    sum_r2x = 0

    for i in pcaobj["r2x"]:
        sum_r2x += i
        y_axis.append(round(sum_r2x, 3))

    if len(x_axis) != len(y_axis):
        raise ValueError("x and y must be the same length")

    num_pcs = len(x_axis)

    sum_r2 = round(y_axis[num_pcs - 1] * 100, 1)

    filename = f"PC - sum(r2x)_{num_pcs} PCs_{sum_r2}%.png"

    # Plot PCs vs sum(R2X) as a line graph
    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis)

    # Line + points in bold
    ax.plot(
        x_axis,
        y_axis,
        marker="o",
        linestyle="-",
        linewidth=1.5,
        markersize=4,
        markeredgewidth=2,
        color="black",
    )

    for x, y in zip(x_axis, y_axis):
        ax.annotate(
            f"{y:.3f}",
            (x, y),
            textcoords="offset points",
            xytext=(-10, 6),
            ha="center",
            fontsize=8,
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

    fig.savefig(f"{SPECTRA_OUTPUT}/{filename}", bbox_inches="tight", dpi=300)
    plt.show()


# ====================================================
# Standard Normal Variate (SNV) preprocessing function
# ====================================================
def standard_normal_variate(intensity_data, spectral_axis):

    intensity_data = np.asarray(intensity_data, dtype=float)

    # If 1D, make it 2D with 1 row
    if intensity_data.ndim == 1:
        intensity_data = intensity_data.reshape(1, -1)

    mean = intensity_data.mean(axis=1, keepdims=True)

    std = intensity_data.std(axis=1, ddof=1, keepdims=True)

    snv_intensity_data = (intensity_data - mean) / std

    return snv_intensity_data, spectral_axis


if __name__ == "__main__":
    main()
