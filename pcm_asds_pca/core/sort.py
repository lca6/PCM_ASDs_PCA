from pcm_asds_pca.config.settings import ANALYSIS_FOLDER
import re

# ==================================================
# Sort files alphabetically by plate number and well
# ==================================================


def sort_files(files):

    # Remove glass reference - later we add back after sort
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
            return (plate, -1, -1)

        # Well-level file
        m = well_pattern.search(filename)
        return (plate, ord(m.group(1)), int(m.group(2)))

    sorted_files = sorted(files, key=sort_key)

    sample_labels = []
    for f in sorted_files:
        if m := well_pattern.search(f):
            location = "(edge)" if edge_pattern.search(f) else "(centre)"
            sample_labels.append(f"{m.group(1)}{m.group(2)} {location}")

    # Add back glass reference
    if glass_reference == True:
        sorted_files.append(f"{ANALYSIS_FOLDER}/glass_reference.txt")
        sample_labels.append("glass reference")

    return sorted_files, sample_labels
