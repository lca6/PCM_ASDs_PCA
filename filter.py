from dotenv import load_dotenv
from os import getenv

load_dotenv()

macbook_url = getenv("MACBOOK_URL")
processing_folder = getenv("PROCESSING_FOLDER")


# Filter samples by rows (e.g. "B")
rows_to_remove = []

# Filter samples by columns (e.g. 5)
cols_to_remove = []

# Crop spectra => to not crop the spectrum: (None, None)
wavenumber_range = (None, None)
