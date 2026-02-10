# ==================================================
# Sort files alphabetically by plate number and well
# ==================================================

from pcm_asds_pca.config.settings import ANALYSIS_FOLDER
import re


def sort_files(files):

    # Remove glass reference temporarily
    glass_reference = False

    if f"{ANALYSIS_FOLDER}/glass_reference.txt" in files:
        glass_reference = True
        files.remove(f"{ANALYSIS_FOLDER}/glass_reference.txt")

    plate_pattern = re.compile(r"plate(\d+)")
    well_pattern = re.compile(r"_([A-H])(\d+)(?:_[^\.]+)?\.txt$")
    edge_pattern = re.compile(r"_edge\.txt$")
    multiwell_pattern = re.compile(r"_multiwell\.txt$")

    def sort_key(filename):
        plate = int(plate_pattern.search(filename).group(1))

        # Multiwell file
        if multiwell_pattern.search(filename):
            return (plate, -1, -1, -1)

        # Well-level file
        m = well_pattern.search(filename)
        row = ord(m.group(1))
        col = int(m.group(2))

        position = 1 if edge_pattern.search(filename) else 0

        return (plate, row, col, position)

    sorted_files = sorted(files, key=sort_key)

    # Add back glass reference at the end
    if glass_reference == True:
        sorted_files.append(f"{ANALYSIS_FOLDER}/glass_reference.txt")

    return sorted_files
