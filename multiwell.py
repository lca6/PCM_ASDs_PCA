# This file loads in Raman spectra obtained using the multiwell function on a plate

# To be read, the files must be in the format [row][column].xy

# The spectral data can then be preprocessed and analysed using Principle Component Analysis (PCA)

# The spectra can also be visualised

import pandas as pd
import numpy as np
import pyphi as phi
import pyphi_plots as pp


import ramanspy as rp
import string

def parse_csv(csv_filename):
    data = pd.read_csv(csv_filename, comment='#')

    # parse and load data into spectral objects
    spectral_data = data["RamanShift(cm-1)"]
    spectral_axis = data["Intensity"]

    raman_spectrum = rp.Spectrum(spectral_data, spectral_axis)

    return raman_spectrum


def main():
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
                raman_spectrum = parse_csv(f'C:/Users/fsb22131/OneDrive - University of Strathclyde/pca/pyphi/spectra_data/csv/{r}{c:02d}.csv')

            except FileNotFoundError:
                continue

            samples.append(raman_spectrum)

            indices.append(f'{r}{c:02d}')

    # Visualising the spectra
    rp.plot.spectra(samples, label=indices, title='Raman spectra in separate graphs')

    rp.plot.show()
    '''
    rp.plot.spectra(samples, label=indices, title='Raman spectra overlaid on one graph', plot_type='single')

    rp.plot.show()

    rp.plot.spectra(samples, label=indices, title='Raman spectra stacked on top of each other', plot_type='stacked')

    rp.plot.show()

    rp.plot.spectra(samples, label=indices, title='Raman spectra stacked on top of each other', plot_type='single stacked')

    rp.plot.show()
    '''

if __name__ == '__main__':
    main()
