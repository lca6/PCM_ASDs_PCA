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

from pcm_asds_pca.config.settings import (
    COLORBY,
    DISPLAY_DIAGNOSTICS,
    DISPLAY_PCs_R2X,
    DISPLAY_SAMPLE_LABELS,
    DISPLAY_SCORE_SCATTER,
    DISPLAY_SPECTRA,
    FIRST_PC,
    PATH_TO_DIR,
    NAME,
    PCA_OUTPUT,
    SECOND_PC,
    SPECTRA_OUTPUT,
)

from pcm_asds_pca.core.sample import Sample


def main():

    # Read pcaobj from .npy file
    pcaobj = np.load(f"{PCA_OUTPUT}/pcaobj_not_viewable.npy", allow_pickle=True).item()

    # Read sample_df from .pkl file
    sample_df = pd.read_pickle(f"{PCA_OUTPUT}/sample_df_not_viewable.pkl")

    # Read num_pcs from pca_settings.json file
    with open(f"{PCA_OUTPUT}/pca_settings.json") as f:
        settings = json.load(f)
        num_pcs = settings["Principle Components"]

    # Create spectra_output folder if it doesn't exist
    folder = pathlib.Path(f"{SPECTRA_OUTPUT}")
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)

    # Create a list of sample labels
    # The label for each sample is in the format: "well (position) (appearance) (plate X)"
    sample_labels = (
        sample_df["well"]
        + " ("
        + sample_df["position"]
        + ")"
        + " ("
        + sample_df["appearance"]
        + ")"
        + " (plate "
        + sample_df["plate"].astype(str)
        + ")"
    ).tolist()

    # Save samples to spectra_samples.txt
    with open(f"{SPECTRA_OUTPUT}/spectra_samples.txt", "w") as f:
        for s in sample_labels:
            print(s, file=f)

    print()
    print(
        f'Please see "{SPECTRA_OUTPUT}/spectra_samples.txt" for a list of the samples displayed.'
    )
    print()

    # ===============================================================================================
    # Display Raman spectra
    # The spectra are preprocessed with the same preprocessing techniques as those applied before PCA
    # This ensures that the spectra visualised are the same as those used for PCA
    # ===============================================================================================
    if DISPLAY_SPECTRA is True:

        display_spectra(sample_df, sample_labels, NAME)

    # ===========================================================================
    # Display a plot of the number of Principle Components (PCs) against sum(R2X)
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
                "First Principle Component must be greater than or equal to 1 and less than or equal to the total number of Principle Components."
            )

        if SECOND_PC < 1 or SECOND_PC > num_pcs:
            sys.exit(
                "Second Principle Component must be greater than or equal to 1 and less than or equal to the total number of Principle Components."
            )

        if SECOND_PC == FIRST_PC:
            sys.exit("Second Principle Component cannot equal the first.")

        # Set title and filename for score scatter and diagnostics plots based on COLORBY, FIRST_PC and SECOND_PC
        if colorby == "none":
            title = f"{NAME} with {num_pcs} Principle Components"
            filename = f"{NAME}_{num_pcs} PCs_PC{FIRST_PC} - PC{SECOND_PC}"
        else:
            title = f"{NAME} coloured by {colorby.capitalize()} with {num_pcs} Principle Components"
            filename = f"{NAME}_{colorby.capitalize()}_{num_pcs} PCs_PC{FIRST_PC} - PC{SECOND_PC}"

        # ========================================================
        # Display score scatter plot of FIRST_PC against SECOND_PC
        # ========================================================
        if colorby == "none":
            pp.score_scatter(
                pcaobj,
                [FIRST_PC, SECOND_PC],
                addtitle=title,
                filename=filename,
            )

        else:
            pp.score_scatter(
                pcaobj,
                [FIRST_PC, SECOND_PC],
                addtitle=title,
                CLASSID=sample_df,
                colorby=colorby,
                filename=filename,
            )

        # ==============================
        # Display Hotelling's T2 and SPE
        # ==============================
        if DISPLAY_DIAGNOSTICS is True:

            pp.diagnostics(
                pcaobj,
                addtitle=title,
                filename=filename,
                score_plot_xydim=[FIRST_PC, SECOND_PC],
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
def display_spectra(sample_df, sample_labels, title):

    title = title.title()

    filename = f"raman_spectrum_{title}"

    # Read wavenumber_range from pca_settings.json file
    with open(f"{PCA_OUTPUT}/pca_settings.json") as f:
        settings = json.load(f)
        wavenumber_range = settings["Wavenumber range"]

    samples = sample_df.index.tolist()

    # To not display sample labels
    if DISPLAY_SAMPLE_LABELS is False:
        sample_labels = None

    pipeline = []

    # Extract preprocessing techniques conducted before PCA
    with open(f"{PCA_OUTPUT}/pca_settings.json") as f:
        settings = json.load(f)
        preprocess_with_savgol = settings["Savitzky-Golay"]
        preprocess_with_snv = settings["Standard Normal Variate"]

    if preprocess_with_snv is True:
        pipeline.append(rp.preprocessing.PreprocessingStep(standard_normal_variate))
        title += " + Standard Normal Variate"
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
        title += " + Savitzky-Golay filter"
        filename += f"_savgol_win{savgol_window}_poly{savgol_polynomial}_deriv{savgol_derivative}"

    if pipeline == []:
        title += " (no preprocessing applied)"
        filename += "_nopreprocessing"

    preprocessing_pipeline = rp.preprocessing.Pipeline(pipeline)

    spectra_to_visualise = []

    for sample in samples:

        # Crop spectra
        cropper = rp.preprocessing.misc.Cropper(region=wavenumber_range)
        spectrum = cropper.apply(sample.spectrum)

        # Preprocess the spectrum with the same preprocessing techniques as those applied before PCA
        preprocessed_spectrum = preprocessing_pipeline.apply(spectrum)

        spectra_to_visualise.append(preprocessed_spectrum)

    # Plot the spectra overlaid on a single axis
    rp.plot.spectra(
        spectra_to_visualise,
        label=sample_labels,
        plot_type="single",
        title=title,
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
