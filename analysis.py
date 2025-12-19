# This file loads in Raman spectral data obtained either manually (singlewell) or autonomously (multiwell)

# The spectral data can then be preprocessed and analysed using Principle Component Analysis

# The spectra can also be visualised


import pandas as pd
import numpy as np
import pyphi as phi
import pyphi_plots as pp
import ramanspy as rp

import string
import sys
import os
import pathlib
import re

from parse import load_spectrum
from dotenv import load_dotenv
from sample import Sample

load_dotenv()

onedrive_url = os.getenv("ONEDRIVE_URL")

PLATE_TO_ANALYSE: int = 2


# To run the singlewell function at the CLI, run the command "python analysis.py -s"
def analyse_spectra_singlewell():

    path = pathlib.Path("spectra_data")
    path = [x for x in path.iterdir() if x.is_file()]

    # Remove unwanted files from analysis such as multiwell files and reference files
    files_to_be_processed = []
    for p in path:
        p = str(p)
        try:
            p.index("multiwell")
        except ValueError:

            for _ in p:
                if _.isupper():
                    files_to_be_processed.append(p)
                else:
                    continue

    samples = []
    dataframes = []
    for file in files_to_be_processed:

        # Loads the Raman object for visualising the spectrum
        spectrum = rp.load.labspec(f"{onedrive_url}{file}")

        sample = Sample(file, spectrum)

        samples.append(sample)

        # Loads spectra from chosen plate into pandas Dataframe for PCA
        if sample.plate == PLATE_TO_ANALYSE:

            with open(f"{onedrive_url}{file}") as f:

                file = []
                for line in f:
                    if line[0] != "#":
                        shift, intensity = line.split("\t", maxsplit=1)
                        file.append(
                            dict(
                                sample=sample.position,
                                shift=shift,
                                intensity=intensity[:-1],
                            )
                        )

                file = pd.DataFrame(file)

                # Convert data to floats before pivoting
                file["shift"] = file["shift"].astype(float)
                file["intensity"] = file["intensity"].astype(float)

                file = file.pivot(index="sample", columns="shift", values="intensity")

                dataframes.append(file)

    # ============
    # Preprocessing
    # =============




    # ============================
    # Principle Component Analysis
    # ============================

    spectral_data = pd.concat(dataframes)

    print(spectral_data)

    pcaobj = phi.pca(spectral_data, 3)







    # =======================
    # Visualising the spectra
    # ========================

    # Choose spectra we want to visualise
    spectra_to_visualise = []
    spectra_labels = []

    for sample in samples:

        # View spectra a chosen plate
        if sample.plate == PLATE_TO_ANALYSE:
            spectra_to_visualise.append(sample.spectrum)
            spectra_labels.append(sample.position)
            plate_num = sample.plate
            conc = sample.concentration

    spectra_labels.sort(
        key=lambda x: (re.findall(r"\D+", x)[0], int(re.findall(r"\d+", x)[0]))
    )

    rp.plot.spectra(
        spectra_to_visualise,
        label=spectra_labels,
        plot_type="single",
        title=f"Plate #{plate_num} Concentration {conc} mg/mL",
    )

    rp.plot.show()


# To run the multiwell function at the CLI, run the command "python analysis.py -m"
def analyse_spectra_multiwell():

    # A-H
    rows = [x for x in string.ascii_uppercase[:8]]

    # 1-12
    columns = [x for x in range(1, 13)]

    # list of raman spectra
    samples = []

    # e.g. A2, B7, C9
    indices = []

    for r in rows:
        for c in columns:

            # Loads the Raman spectra for visualising the spectra
            try:
                raman_spectrum = load_spectrum(
                    f"{onedrive_url}spectra_data/csv/{r}{c}.csv"
                )

            except FileNotFoundError:
                continue

            samples.append(raman_spectrum)

            indices.append(f"{r}{c}")

    # Visualising the spectra
    rp.plot.spectra(samples, label=None, title="Raman spectra", plot_type="single")

    rp.plot.show()


def main():

    ERROR = "Please specify which function you would like to run\nRun python analysis.py -s for the singlewell function\nRun python analysis.py -m for the multiwell function"

    if len(sys.argv) != 2:
        sys.exit(ERROR)
    elif sys.argv[1] == "-s":
        analyse_spectra_singlewell()
    elif sys.argv[1] == "-m":
        analyse_spectra_multiwell()
    else:
        sys.exit(ERROR)


if __name__ == "__main__":
    main()
