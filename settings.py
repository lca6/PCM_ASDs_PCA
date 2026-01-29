from dotenv import load_dotenv
from os import getenv

load_dotenv()

ANALYSIS_FOLDER = getenv("ANALYSIS_FOLDER")
MACBOOK_URL = getenv("MACBOOK_URL")
OUTPUT_FOLDER = getenv("OUTPUT_FOLDER")

# Choose parameter to colour by
COLORBY = "drug_loading"

# Filter samples by columns (e.g. 5)
COLS_TO_REMOVE = []

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

# Toggle whether to display spectra
DISPLAY_SPECTRA = False

# Principle Components that you would like to plot - FIRST_PC on the x-axis
FIRST_PC = 1

# Name of plots and files
NAME = "plates 2 & 3"

# Number of Principle Components
NUM_PCS = 3

# Filter samples by rows (e.g. "B")
ROWS_TO_REMOVE = []

# Toggle whether to display sample labels
SAMPLE_LABELS = False

# Savitzky-Golay filter parameters
SAVGOL = False

SAVGOL_DERIVATIVE = 0

SAVGOL_POLYNOMIAL = 3

SAVGOL_WINDOW = 7

# Principle Components that you would like to plot - SECOND_PC on the y-axis
SECOND_PC = 2

# Crop spectra => to not crop the spectrum: (None, None)
WAVENUMBER_RANGE = (None, None)
