import pandas as pd
import numpy as np
import pyphi as phi
import pyphi_plots as pp


import ramanspy as rp
import string


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
        
        # Loads the Raman spectra
        try:
            raman_object = rp.load.labspec(f'C:/Users/fsb22131/OneDrive - University of Strathclyde/pca/pyphi/spectra_data/{r}{c}_20251112_PCM_01.txt')

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

        with open(f'C:/Users/fsb22131/OneDrive - University of Strathclyde/pca/pyphi/spectra_data/{r}{c}_20251112_PCM_01.txt') as f:

            # File is a list of dictionaries
            file = [] 
            for line in f:
                if line[0] != '#':
                    shift, intensity = line.split('\t', maxsplit=1)
                    file.append(dict(sample=f'{r}{c}', shift=shift, intensity=intensity[:-1]))
            
            # File is a dataframe
            file = pd.DataFrame(file).pivot(index='sample', columns='shift', values='intensity')

            spectra_dataframes.append(pd.DataFrame(file))

dataset = pd.concat(spectra_dataframes)

# With this dataset we can complete PCA




# Visualising the spectra
'''
rp.plot.spectra(samples, label=indices, title='Raman spectra in separate graphs')

rp.plot.show()

rp.plot.spectra(samples, label=indices, title='Raman spectra overlaid on one graph', plot_type='single')

rp.plot.show()

rp.plot.spectra(samples, label=indices, title='Raman spectra stacked on top of each other', plot_type='stacked')

rp.plot.show()

rp.plot.spectra(samples, label=indices, title='Raman spectra stacked on top of each other', plot_type='single stacked')

rp.plot.show()
'''








