import matplotlib.pyplot as plt
import ramanspy as rp

from contextlib import redirect_stdout, redirect_stderr

from filter import (
    ROWS_TO_REMOVE,
    COLS_TO_REMOVE,
    MACBOOK_URL,
    OUTPUT_FOLDER,
    WAVENUMBER_RANGE,
    sort_files,
)
from matplotlib.ticker import MaxNLocator
from sample import Sample


# ========================
# Visualising the spectra
# ========================


def display_spectra(files, title):

    files, sample_labels = sort_files(files)

    plate = []
    spectra_to_visualise = []

    i = ""
    while i not in ["Y", "N"]:
        i = input("Display sample labels (Y/N): ").capitalize()
        print()

    if i == "Y":
        sample_labels = sample_labels
    elif i == "N":
        sample_labels = None

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

        spectra_to_visualise.append(spectrum)

    # Prints samples to spectra_samples.txt
    with open(f"{OUTPUT_FOLDER}/spectra_samples.txt", "w") as f:
        with redirect_stdout(f), redirect_stderr(f):
            for sample in plate:
                print(sample)

    rp.plot.spectra(
        spectra_to_visualise,
        label=sample_labels,
        plot_type="single",
        title="Raman spectrum - " + title,
    )

    plt.savefig(f"raman_spectrum_{title}")
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