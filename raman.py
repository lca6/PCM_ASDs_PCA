import pandas as pd
import numpy as np
import pyphi as phi
import pyphi_plots as pp


import ramanspy as rp
import string


# List of .txt files as dictionaries
spectra_txt_files = []

# then converted into pandas DataFrames for being read by pyphi
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
            
            file = []
            p = 0
            for line in f:
                if line[0] != '#':
                    p += 1
                    shift, intensity = line.split('\t', maxsplit=1)
                    file.append(dict(point=p, shift=shift, intensity=intensity[:-1]))

            spectra_txt_files.append(file)       


# Convert dictionaries (d) into pandas DataFrames (df)
for d in spectra_txt_files:
    df = pd.DataFrame(d)
    spectra_dataframes.append(df)









# Visualising the spectra
"""
rp.plot.spectra(samples, label=indices, title='Raman spectra in separate graphs')

rp.plot.show()

rp.plot.spectra(samples, label=indices, title='Raman spectra overlaid on one graph', plot_type='single')

rp.plot.show()

rp.plot.spectra(samples, label=indices, title='Raman spectra stacked on top of each other', plot_type='stacked')

rp.plot.show()

rp.plot.spectra(samples, label=indices, title='Raman spectra stacked on top of each other', plot_type='single stacked')

rp.plot.show()
"""








