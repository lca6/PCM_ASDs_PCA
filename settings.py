from dotenv import load_dotenv
from os import getenv

load_dotenv()

MACBOOK_URL = getenv("MACBOOK_URL")
ANALYSIS_FOLDER = getenv("ANALYSIS_FOLDER")
OUTPUT_FOLDER = getenv("OUTPUT_FOLDER")


# Filter samples by rows (e.g. "B")
ROWS_TO_REMOVE = []

# Filter samples by columns (e.g. 5)
COLS_TO_REMOVE = []

# Crop spectra => to not crop the spectrum: (None, None)
WAVENUMBER_RANGE = (None, None)

# Savitzky-Golay filter parameters
SAVGOL_WINDOW = 7

SAVGOL_POLYNOMIAL = 3

SAVGOL_DERIVATIVE = 0