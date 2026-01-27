from dotenv import load_dotenv
from os import getenv
import re

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


def sort_files(files):

    glass_reference = False

    if f"{ANALYSIS_FOLDER}/glass_reference.txt" in files:
        glass_reference = True
        files.remove(f"{ANALYSIS_FOLDER}/glass_reference.txt")

    plate_pattern = re.compile(r"plate(\d+)")
    well_pattern = re.compile(r"_([A-H])(\d+)(?:_[^\.]+)?\.txt$")
    multiwell_pattern = re.compile(r"_multiwell\.txt$")

    def sort_key(filename):
        plate = int(plate_pattern.search(filename).group(1))

        # Multiwell file: no row/column
        if multiwell_pattern.search(filename):
            return (plate, -1, -1)  # sorts before well-level files

        # Well-level file
        m = well_pattern.search(filename)
        return (plate, ord(m.group(1)), int(m.group(2)))

    sorted_files = sorted(files, key=sort_key)

    sample_labels = []
    for f in sorted_files:
        m = well_pattern.search(f)
        if m:
            sample_labels.append(f"{m.group(1)}{m.group(2)}")
        else:
            sample_labels.append("multiwell")

    if glass_reference == True:
        sorted_files.append(f"{ANALYSIS_FOLDER}/glass_reference.txt")
        sample_labels.append("glass reference")

    return sorted_files, sample_labels
