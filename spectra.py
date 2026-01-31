import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pathlib
import pyphi.pyphi_plots as pp
import ramanspy as rp
import shutil
import sys
import time

from matplotlib.ticker import MaxNLocator

from sample import Sample

from settings import (
    COLORBY,
    COLS_TO_REMOVE,
    DISPLAY_DIAGNOSTICS,
    DISPLAY_PCs_R2X, 
    DISPLAY_SCORE_SCATTER,
    DISPLAY_SPECTRA,
    FIRST_PC,
    MACBOOK_URL,
    NAME,
    NUM_PCS,
    PCA_OUTPUT,
    ROWS_TO_REMOVE,
    SAMPLE_LABELS,
    PREPROCESS_WITH_SAVGOL,
    PREPROCESS_WITH_SNV,
    SAVGOL_DERIVATIVE,
    SAVGOL_POLYNOMIAL,
    SAVGOL_WINDOW,
    SECOND_PC,
    SPECTRA_OUTPUT,
    WAVENUMBER_RANGE,
)

from sort import sort_files


def main():

    # Read pcaobj from npy file
    pcaobj = np.load(f"{PCA_OUTPUT}/pcaobj_not_viewable.npy", allow_pickle=True).item()

    if DISPLAY_SPECTRA is True:

        # Read parsed_files from txt file
        with open(f"{PCA_OUTPUT}/parsed_files.txt") as f:
            parsed_files = json.load(f)

        display_spectra(parsed_files, NAME)

    if DISPLAY_PCs_R2X is True:

        x = [x for x in range(1, NUM_PCS + 1)]

        y = []
        sum_r2x = 0

        for i in pcaobj["r2x"]:
            sum_r2x += i
            y.append(round(sum_r2x, 3))

        display_PCs_R2X(x, y)

    if DISPLAY_SCORE_SCATTER is True:

        sample_df = pd.read_pickle(f"{PCA_OUTPUT}/sample_df_not_viewable.pkl")

        options = []
        for i in sample_df.columns:
            options.append(i)
        options.append("none")

        if COLORBY.lower() not in options:
            sys.exit(
                f"Column does not exist. Cannot colour by this parameter. Options: {options}\n"
            )

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
            FILENAME = f"{NAME}_{COLORBY.capitalize()}_{NUM_PCS} PCs_PC{FIRST_PC} - PC{SECOND_PC}"

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
                pcaobj,
                addtitle=TITLE,
                filename=FILENAME,
                score_plot_xydim=[FIRST_PC, SECOND_PC],
            )

    # Wait for plots to load in browser
    time.sleep(5)

    # Move html files to spectra_output
    src_dir = pathlib.Path(".")
    dst_dir = pathlib.Path(f"{SPECTRA_OUTPUT}")
    dst_dir.mkdir(parents=True, exist_ok=True)

    for html_file in src_dir.glob("*.html"):
        shutil.move(html_file, dst_dir / html_file.name)



# ========================
# Visualising the spectra
# ========================


def display_spectra(files, title):

    title = title.title()

    filename = f"raman_spectrum_{title}"

    files, sample_labels = sort_files(files)

    if SAMPLE_LABELS is True:
        sample_labels = sample_labels
    elif SAMPLE_LABELS is False:
        sample_labels = None

    pipeline = []

    if PREPROCESS_WITH_SAVGOL is True:
        pipeline.append(
            rp.preprocessing.denoise.SavGol(
                window_length=SAVGOL_WINDOW,
                polyorder=SAVGOL_POLYNOMIAL,
                deriv=SAVGOL_DERIVATIVE,
            )
        )
        title = title + " + Savitzky-Golay filter"
        filename += f"_savgol_win{SAVGOL_WINDOW}_poly{SAVGOL_POLYNOMIAL}_deriv{SAVGOL_DERIVATIVE}"

    if PREPROCESS_WITH_SNV is True:
        pipeline.append(
            rp.preprocessing.PreprocessingStep(standard_normal_variate)
        )
        title = title + " + Standard Normal Variate"
        filename += "_snv"

    preprocessing_pipeline = rp.preprocessing.Pipeline(pipeline)

    plate = []
    spectra_to_visualise = []

    for file in files:

        # Loads the Raman object for visualising the spectrum
        spectrum = rp.load.labspec(f"{MACBOOK_URL}{file}")

        sample = Sample(file, spectrum)

        plate.append(sample)

        # Filter spectra to be visualised
        if sample.row in ROWS_TO_REMOVE:
            continue
        elif sample.col in COLS_TO_REMOVE:
            continue

        # Crop spectra
        cropper = rp.preprocessing.misc.Cropper(region=WAVENUMBER_RANGE)
        spectrum = cropper.apply(sample.spectrum)

        # Preprocess the spectrum
        preprocessed_spectrum = preprocessing_pipeline.apply(spectrum)

        spectra_to_visualise.append(preprocessed_spectrum)

    # Prints samples to spectra_samples.txt
    with open(f"{SPECTRA_OUTPUT}/spectra_samples.txt", "w") as f:
        for sample in plate:
            print(sample, file=f)

    rp.plot.spectra(
        spectra_to_visualise,
        label=sample_labels,
        plot_type="single",
        title=title,
    )

    plt.savefig(f"{SPECTRA_OUTPUT}/{filename}", bbox_inches="tight", dpi=300)
    plt.show()

    print(
        f'Please see "{SPECTRA_OUTPUT}/spectra_samples.txt" for a list of the samples displayed.'
    )
    print()


# ====================================================
# Plot number of principle components against sum(R2X)
# ====================================================


def display_PCs_R2X(x_axis, y_axis):

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
