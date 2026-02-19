# ===================================================
#  Configuration settings for PCA analysis of spectra
# ===================================================

from dotenv import load_dotenv
import numpy as np
from os import getenv

load_dotenv()

PATH_TO_DIR = getenv("PATH_TO_DIR")

ANALYSIS_FOLDER = "analyse"
PCA_OUTPUT = "pca_output"
SPECTRA_OUTPUT = "spectra_output"

# ================
# Configure pca.py
# ================

# Toggle whether to conduct PCA
CONDUCT_PCA = False

# Number of Principle Components
NUM_PCS = 0

# Filter samples by plate (e.g. 2)
PLATES_TO_REMOVE_IN_PCA = []

# Filter samples by rows (e.g. "B")
ROWS_TO_REMOVE_IN_PCA = []

# Filter samples by columns (e.g. 5)
COLS_TO_REMOVE_IN_PCA = []

# Filter samples by appearance
# To not filter: ""
# To remove crystalline samples: "crystalline"
# To remove amorphous samples: "amorphous"
APPEARANCE_TO_REMOVE_IN_PCA = ""

# Crop spectra: (None, None) defaults to 0 and 2000 cm-1 respectively
# Otherwise must be integers between 0 and 2000
WAVENUMBER_RANGE = (None, None)

# % of data to remove per round of PCA
# Must be an integer between 0 and 100
CROSS_VAL = 0

# Toggle preprocessing with Standard Normal Variate
PREPROCESS_WITH_SNV = False

# Toggle preprocessing with Savitzky-Golay filter
PREPROCESS_WITH_SAVGOL = False

# Savitzky-Golay filter parameters
SAVGOL_DERIVATIVE = 0

SAVGOL_POLYNOMIAL = 0

SAVGOL_WINDOW = 0

# =====================
# Configure settings.py
# =====================

# Name of plots and files
NAME = ""

# Toggle whether to filter pcaobj
FILTER_PCAOBJ = False

# Toggle whether to display score scatter
DISPLAY_SCORE_SCATTER = False

# Choose parameter to colour by
# To not colour: "none"
COLORBY = "none"

# Filter spectra by plate (e.g. 2)
# Remember to change NAME accordingly
PLATES_TO_REMOVE_IN_SPECTRA = []

# Filter spectra by rows (e.g. "B")
ROWS_TO_REMOVE_IN_SPECTRA = []

# Filter spectra by columns (e.g. 5)
COLS_TO_REMOVE_IN_SPECTRA = []

# Toggle whether to display spectra
DISPLAY_SPECTRA = False

# Toggle whether to display sample labels
DISPLAY_SAMPLE_LABELS = False

# Principle Components that you would like to plot - FIRST_PC on the x-axis
FIRST_PC = 0

# Principle Components that you would like to plot - SECOND_PC on the y-axis
SECOND_PC = 0

# Toggle whether to display plot of PCs vs sum(R2X)
DISPLAY_PCs_R2X = False

# Toggle whether to display diagnostics
# Hotelling's T2 and SPE
DISPLAY_DIAGNOSTICS = False


def filter_pcaobj(pcaobj, rows_to_remove=None):
    if rows_to_remove is None:
        rows_to_remove = []

    if FILTER_PCAOBJ == False:
        return pcaobj, rows_to_remove

    first_pc_column_index = FIRST_PC - 1
    second_pc_column_index = SECOND_PC - 1

    for row_index, row in enumerate(pcaobj["T"]):

        # Filter pcaobj by coordinate on score scatter plot
        if row[first_pc_column_index] > 0:
            rows_to_remove.append(row_index)
        elif row[second_pc_column_index] > 0:
            rows_to_remove.append(row_index)

    pcaobj["T"] = np.delete(pcaobj["T"], rows_to_remove, axis=0)

    pcaobj["obsidX"] = [obsid for i, obsid in enumerate(pcaobj["obsidX"]) if i not in rows_to_remove]

    print(pcaobj)

    return pcaobj, rows_to_remove
    