import pathlib
import sys

from filter import macbook_url, processing_folder


def main():

    file = pathlib.Path(processing_folder)
    file = [str(x) for x in file.iterdir()]

    if len(file) > 1:
        sys.exit("Too many files")

    if len(file) < 1:
        sys.exit("Please provide a multiwell file")

    if len(file) == 1:
        file = file[0]

    plate_info = file.removeprefix(f"{processing_folder}/").removesuffix(
        "_multiwell.txt"
    )

    plate_num, plate_conc = plate_info.split("_")

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

    with open(file, encoding="latin-1") as f:
        text = f.read()

    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

    output_dir = f"{macbook_url}{processing_folder}/"

    header, spectra = parse_multiwell_file(pathlib.Path(file))
    write_txt(header, spectra, pathlib.Path(output_dir), plate_num, plate_conc)

    # Remove multiwell file once parsed
    pathlib.Path(file).unlink()


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


def write_txt(header, spectra, outdir, plate_number, plate_concentration):
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


if __name__ == "__main__":
    main()
