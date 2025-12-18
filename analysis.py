# This file loads in Raman spectral data obtained either manually (singlewell) or autonomously (multiwell)

# The spectral data can then be preprocessed and analysed using Principle Component Analysis (PCA)

# The spectra can also be visualised


import pandas as pd
import numpy as np
import pyphi as phi
import pyphi_plots as pp
import ramanspy as rp

import string
import sys
import os

from parse import parse_csv
from dotenv import load_dotenv

load_dotenv()

onedrive_url = os.getenv("ONEDRIVE_URL")



# To run the singlewell function at the CLI, run the command "python analysis.py -s"
def load_spectra_singlewell():

    # List of .txt files as pandas DataFrames
    spectra_dataframes = []

    # list of dictionaries
    # each entry consists of a raman_object and its index (e.g. A2)
    plate = []

    # list of raman_objects
    samples = []

    # e.g. A2, B7, C9
    indices = []

    # A-H
    rows = [x for x in string.ascii_uppercase[:8]]

    # 1-12
    columns = [x for x in range(1, 13)]

    for r in rows:
        for c in columns:
            
            # Loads the Raman spectra for visualising the spectra
            try:
                raman_object = rp.load.labspec(f'{onedrive_url}spectra_data/{r}{c}_20251112_PCM_01.txt')

            except FileNotFoundError:
                continue

            samples.append(raman_object)

            indices.append(f'{r}{c}')

            sample = {
                "raman_object": raman_object,
                "index": f"{r}{c}"
            }

            plate.append(sample)


            # Loads spectrum into pandas Dataframe for PCA
            with open(f'{onedrive_url}spectra_data/{r}{c}_20251112_PCM_01.txt') as f:

                file = [] 
                for line in f:
                    if line[0] != '#':
                        shift, intensity = line.split('\t', maxsplit=1)
                        file.append(dict(sample=f'{r}{c}', shift=shift, intensity=intensity[:-1]))
                
                file = pd.DataFrame(file)

                # Convert data to floats before pivoting
                file['shift'] = file['shift'].astype(float)
                file['intensity'] = file['intensity'].astype(float)
                
                file = file.pivot(index='sample', columns='shift', values='intensity')

                spectra_dataframes.append(file)

    # Preprocessing


    # With this dataset we can complete PCA
    raman_spectra = pd.concat(spectra_dataframes)

    pcaobj = phi.pca(raman_spectra, 3)




    # Visualising the spectra
    rp.plot.spectra(samples, label=indices, title='Raman spectra in separate graphs')

    rp.plot.show()

    rp.plot.spectra(samples, label=indices, title='Raman spectra overlaid on one graph', plot_type='single')

    rp.plot.show()

    rp.plot.spectra(samples, label=indices, title='Raman spectra stacked on top of each other', plot_type='stacked')

    rp.plot.show()

    rp.plot.spectra(samples, label=indices, title='Raman spectra stacked on top of each other', plot_type='single stacked')

    rp.plot.show()






# To run the multiwell function at the CLI, run the command "python analysis.py -m"
def load_spectra_multiwell():

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
                raman_spectrum = parse_csv(f"{onedrive_url}spectra_data/{r}{c:02d}.csv")

            except FileNotFoundError:
                continue

            samples.append(raman_spectrum)

            indices.append(f'{r}{c}')

    # Visualising the spectra
    rp.plot.spectra(samples, label=None, title="Raman spectra", plot_type="single")

    rp.plot.show()




def main():

    ERROR = "Please specify which function you would like to run\nRun python analysis.py -s for the singlewell function\nRun python analysis.py -m for the multiwell function"

    if len(sys.argv) != 2:
        sys.exit(ERROR)
    elif sys.argv[1] == "-s":
        load_spectra_singlewell()
    elif sys.argv[1] == "-m":
        load_spectra_multiwell()
    else:
        sys.exit(ERROR)

if __name__ == "__main__":
    main()