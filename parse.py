import pathlib
import shutil
import sys

from settings import ANALYSIS_FOLDER, DISPLAY_PARSED_FILES, MACBOOK_URL
from sort import sort_files

# =========================================================================
# Parse all files that end with "_multiwell.txt" and ignore all other files
# Output individual spectra to .txt files
# =========================================================================


def parse():

    files = pathlib.Path(ANALYSIS_FOLDER)
    files = [str(x) for x in files.iterdir()]

    # Confirm samples have been provided
    try:
        files[0]
    except IndexError:
        sys.exit("No files provided")

    # Sorts the order that the files are parsed
    files, _ = sort_files(files)

    for file in files:

        if "_multiwell.txt" not in file:

            if DISPLAY_PARSED_FILES is True:
                print(f"{file} was not parsed")
            continue

        plate_num, plate_conc = (
            file.removeprefix(f"{ANALYSIS_FOLDER}/")
            .removesuffix("_multiwell.txt")
            .split("_")
        )

        plate_num = plate_num.removeprefix("plate")

        try:
            int(plate_num)
        except TypeError:
            sys.exit("Plate number not found")

        plate_conc = plate_conc.removesuffix("mgml")

        try:
            int(plate_conc)
        except TypeError:
            sys.exit("Plate concentration not found")

        # Convert files from latin-1 to utf-8 for parsing
        with open(file, encoding="latin-1") as f:
            text = f.read()

        with open(file, "w", encoding="utf-8") as f:
            f.write(text)

        output_dir = f"{MACBOOK_URL}{ANALYSIS_FOLDER}/"

        header, spectra = parse_multiwell_file(pathlib.Path(file))
        write_txt_file(header, spectra, pathlib.Path(output_dir), plate_num, plate_conc)

        if DISPLAY_PARSED_FILES is True:
            print(f"{file} was parsed")

        # Move multiwell file to Bin once parsed
        trash = pathlib.Path.home() / ".Trash"
        shutil.move(str(file), trash / file.name)

    files = pathlib.Path(ANALYSIS_FOLDER)
    files = [str(x) for x in files.iterdir()]

    # Sorts the order that the files are returned by the function
    files, sample_labels = sort_files(files)
    print()

    # Convert files from latin-1 to utf-8 for visualising the spectra and for PCA
    for file in files:
        with open(file, encoding="latin-1") as f:
            text = f.read()

        with open(file, "w", encoding="utf-8") as f:
            f.write(text)

    return files, sample_labels


# =====================
# Core parsing logic
# =====================


def parse_multiwell_file(path):
    header = []
    data_lines = []

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                header.append(line)
            else:
                data_lines.append(line)

    if len(data_lines) < 2:
        raise ValueError("No spectral data found in file")

    # First non-header line = shared Raman shift axis
    x_vals = list(map(float, data_lines[0].split()))

    spectra = []

    for line in data_lines[1:]:
        parts = line.split()

        # LabRAM export order:
        #   parts[0] = file Column index
        #   parts[1] = file Row index
        file_col = int(parts[0])
        file_row = int(parts[1])

        # IMPORTANT:
        # For this acquisition:
        #   file Column (1–8)  → plate Row (A–H)
        #   file Row    (1–12) → plate Column (1–12)
        plate_row = file_col
        plate_col = file_row

        intensities = list(map(float, parts[2:]))

        if len(intensities) != len(x_vals):
            raise ValueError(f"Length mismatch at file Col={file_col}, Row={file_row}")

        spectra.append((plate_row, plate_col, x_vals, intensities))

    return header, spectra


# =====================
# Output logic
# =====================


def write_txt_file(header, spectra, outdir, plate_number, plate_concentration):
    outdir.mkdir(parents=True, exist_ok=True)

    for row, col, x, y in spectra:

        well = rowcol_to_well(row, col)

        out = outdir / f"plate{plate_number}_{plate_concentration}mgml_{well}.txt"

        with open(out, "w", encoding="utf-8", newline="\n") as f:
            for xi, yi in zip(x, y):
                f.write(f"{xi:.6f}\t{yi:.6f}\n")


# =====================
# Plate utilities
# =====================


def rowcol_to_well(row, col):
    """
    Plate convention:
      Row    = A–H (1–8)
      Column = 01–12
    """
    if not (1 <= row <= 26):
        raise ValueError(f"Row out of range: {row}")
    return f"{chr(64 + row)}{col}"
