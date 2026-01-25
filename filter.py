from dotenv import load_dotenv
from os import getenv
import re

load_dotenv()

MACBOOK_URL = getenv("MACBOOK_URL")
ANALYSIS_FOLDER = getenv("ANALYSIS_FOLDER")


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

    # Plate number, row letter, column number
    pattern = re.compile(r"plate(\d+)_.*_([A-H])(\d+)(?:_|\.txt)")

    sorted_files = sorted(
        files,
        key=lambda x: (
            int(pattern.search(x).group(1)),  # plate number
            pattern.search(x).group(2),  # row letter
            int(pattern.search(x).group(3)),  # column number
        ),
    )

    sample_labels = [
        f"{m.group(2)}{m.group(3)}"
        for f in sorted_files
        if (m := pattern.search(f)) is not None
    ]

    if glass_reference == True:
        sorted_files.append(f"{ANALYSIS_FOLDER}/glass_reference.txt")
        sample_labels.append("glass reference")

    return sorted_files, sample_labels
