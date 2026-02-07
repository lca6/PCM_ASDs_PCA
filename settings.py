from dotenv import load_dotenv
from os import getenv

load_dotenv()

ANALYSIS_FOLDER = getenv("ANALYSIS_FOLDER")
MACBOOK_URL = getenv("MACBOOK_URL")
PCA_OUTPUT = getenv("PCA_OUTPUT")
SPECTRA_OUTPUT = getenv("SPECTRA_OUTPUT")

# Filter samples by rows (e.g. "B")
ROWS_TO_REMOVE = []

# Filter samples by columns (e.g. 5)
COLS_TO_REMOVE = []

# Crop spectra => to not crop the spectrum: (None, None)
WAVENUMBER_RANGE = (None, None)

# Toggle whether to conduct PCA
CONDUCT_PCA = False

# % of data to remove per round of PCA (must be an integer between 0 and 100)
CROSS_VAL = 0

# Toggle whether to display diagnostics (Hotelling's T2 and SPE)
DISPLAY_DIAGNOSTICS = False

# Toggle whether to display parsed files in the terminal
DISPLAY_PARSED_FILES = False

# Toggle whether to display plot of PCs vs sum(R2X)
DISPLAY_PCs_R2X = False

# Toggle whether to display score scatter
DISPLAY_SCORE_SCATTER = False

# Choose parameter to colour by (to not colour: "none")
COLORBY = "none"

# Toggle whether to display spectra
DISPLAY_SPECTRA = False

# Toggle whether to display sample labels
DISPLAY_SAMPLE_LABELS = False

# Number of Principle Components
NUM_PCS = 5

# Principle Components that you would like to plot - FIRST_PC on the x-axis
FIRST_PC = 1

# Principle Components that you would like to plot - SECOND_PC on the y-axis
SECOND_PC = 2

# Name of plots and files
NAME = ""

# Toggle preprocessing with Savitzky-Golay filter
PREPROCESS_WITH_SAVGOL = False

# Savitzky-Golay filter parameters
SAVGOL_DERIVATIVE = 0

SAVGOL_POLYNOMIAL = 0

SAVGOL_WINDOW = 0

# Toggle preprocessing with Standard Normal Variate
PREPROCESS_WITH_SNV = False
