from dotenv import load_dotenv
from os import getenv
import re

load_dotenv()

macbook_url = getenv("MACBOOK_URL")
processing_folder = getenv("PROCESSING_FOLDER")


# Filter samples by rows (e.g. "B")
rows_to_remove = []

# Filter samples by columns (e.g. 5)
cols_to_remove = []

# Crop spectra => to not crop the spectrum: (None, None)
wavenumber_range = (None, None)


def sort_files(files_to_be_sorted):

    glass_reference = False

    if "to_be_processed/glass_reference.txt" in files_to_be_sorted:
        glass_reference = True
        files_to_be_sorted.remove("to_be_processed/glass_reference.txt")

    pattern = re.compile(r"_([A-H])(\d+)(?:_|\.txt)")

    sorted_files = sorted(
        files_to_be_sorted,
        key=lambda x: (pattern.search(x).group(1), int(pattern.search(x).group(2))),
    )

    sample_labels = list(
        map(
            lambda x: f"{x.group(1)}{x.group(2)}",
            filter(None, (pattern.search(f) for f in files_to_be_sorted)),
        )
    )

    sorted_sample_labels = sorted(sample_labels, key=lambda x: (x[0], int(x[1:])))

    if glass_reference == True:
        sorted_files.append("to_be_processed/glass_reference.txt")
        sorted_sample_labels.append("glass reference")

    return sorted_files, sorted_sample_labels
