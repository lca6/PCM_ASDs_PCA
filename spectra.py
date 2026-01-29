import matplotlib.pyplot as plt
import ramanspy as rp

from contextlib import redirect_stdout, redirect_stderr

from matplotlib.ticker import MaxNLocator
from sample import Sample

from settings import (
    ROWS_TO_REMOVE,
    COLS_TO_REMOVE,
    MACBOOK_URL,
    OUTPUT_FOLDER,
    WAVENUMBER_RANGE,
    SAVGOL_WINDOW,
    SAVGOL_POLYNOMIAL,
    SAVGOL_DERIVATIVE,
)

from sort import sort_files

# ========================
# Visualising the spectra
# ========================


def display_spectra(files, title, savgol):

    TITLE = title
    filename = f"raman_spectrum_{title}"

    files, sample_labels = sort_files(files)

    i = ""
    while i not in ["Y", "N"]:
        i = input("Display sample labels (Y/N): ").capitalize()
        print()

    if i == "Y":
        sample_labels = sample_labels
    elif i == "N":
        sample_labels = None

    pipeline = []

    if savgol is True:
        pipeline.append(
            rp.preprocessing.denoise.SavGol(
                window_length=SAVGOL_WINDOW,
                polyorder=SAVGOL_POLYNOMIAL,
                deriv=SAVGOL_DERIVATIVE,
            )
        )
        TITLE = title + f" with Savitzky-Golay filter"
        filename += f"_savgol_win{SAVGOL_WINDOW}_poly{SAVGOL_POLYNOMIAL}_deriv{SAVGOL_DERIVATIVE}"

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
    with open(f"{OUTPUT_FOLDER}/spectra_samples.txt", "w") as f:
        with redirect_stdout(f), redirect_stderr(f):
            for sample in plate:
                print(sample)

    rp.plot.spectra(
        spectra_to_visualise,
        label=sample_labels,
        plot_type="single",
        title=TITLE,
    )

    plt.savefig(filename)
    plt.show()

    print(
        f'Please see "{OUTPUT_FOLDER}/spectra_samples.txt" for a list of the samples displayed.'
    )
    print()


# ====================================================
# Plot number of principle components against sum(R2X)
# ====================================================


def display_PCs_R2X(x_axis, y_axis):

    if len(x_axis) != len(y_axis):
        raise ValueError("x and y must be the same length")

    filename = f"PC - sum(r2x)_{len(x_axis)} PCs.png"

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
