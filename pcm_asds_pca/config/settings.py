# ===================================================
#  Configuration settings for PCA analysis of spectra
# ===================================================

from dotenv import load_dotenv
from os import getenv

load_dotenv()

PATH_TO_DIR = getenv("PATH_TO_DIR")

ANALYSIS_FOLDER = "analyse"
PCA_OUTPUT = "pca_output"
SPECTRA_OUTPUT = "spectra_output"

# Filter samples by plate (e.g. 2)
PLATES_TO_REMOVE = []

# Filter samples by rows (e.g. "B")
ROWS_TO_REMOVE = []

# Filter samples by columns (e.g. 5)
COLS_TO_REMOVE = []

# Filter samples by appearance
# To not filter: ""
# To remove crystalline samples: "crystalline"
# To remove amorphous samples: "amorphous"
APPEARANCE = ""

# Crop spectra: (None, None) defaults to 0 and 2000 cm-1 respectively
# Otherwise must be integers between 0 and 2000
WAVENUMBER_RANGE = (None, None)

# Toggle whether to conduct PCA
CONDUCT_PCA = False

# % of data to remove per round of PCA
# Must be an integer between 0 and 100
CROSS_VAL = 0

# Toggle whether to display diagnostics
# Hotelling's T2 and SPE
DISPLAY_DIAGNOSTICS = False

# Toggle whether to display plot of PCs vs sum(R2X)
DISPLAY_PCs_R2X = False

# Toggle whether to display score scatter
DISPLAY_SCORE_SCATTER = False

# Choose parameter to colour by
# To not colour: "none"
COLORBY = "none"

# Toggle whether to display spectra
DISPLAY_SPECTRA = False

# Toggle whether to display sample labels
DISPLAY_SAMPLE_LABELS = False

# Number of Principle Components
NUM_PCS = 0

# Principle Components that you would like to plot - FIRST_PC on the x-axis
FIRST_PC = 0

# Principle Components that you would like to plot - SECOND_PC on the y-axis
SECOND_PC = 0

# Name of plots and files
NAME = ""

# Toggle preprocessing with Standard Normal Variate
PREPROCESS_WITH_SNV = False

# Toggle preprocessing with Savitzky-Golay filter
PREPROCESS_WITH_SAVGOL = False

# Savitzky-Golay filter parameters
SAVGOL_DERIVATIVE = 0

SAVGOL_POLYNOMIAL = 0

SAVGOL_WINDOW = 0
