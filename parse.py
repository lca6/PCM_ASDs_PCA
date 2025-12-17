import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

import pandas as pd
import ramanspy as rp

# =====================
# Configuration
# =====================

USE_WELL_LABELS = True  # A01, B02, etc.

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
    return f"{chr(64 + row)}{col:02d}"

# =====================
# Core parsing logic
# =====================

def parse_plate_file(path):
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
            raise ValueError(
                f"Length mismatch at file Col={file_col}, Row={file_row}"
            )

        spectra.append((plate_row, plate_col, x_vals, intensities))

    return header, spectra

# =====================
# Output logic
# =====================

def write_csv(header, spectra, outdir):
    outdir.mkdir(parents=True, exist_ok=True)

    for row, col, x, y in spectra:
        if USE_WELL_LABELS:
            name = rowcol_to_well(row, col)
        else:
            name = f"R{row:02d}_C{col:02d}"

        out = outdir / f"{name}.csv"

        with open(out, "w", encoding="utf-8", newline="\n") as f:
            for h in header:
                f.write(h + "\n")
            f.write(f"#PlateRow={row}, PlateColumn={col}\n")
            f.write("RamanShift(cm-1),Intensity\n")
            for xi, yi in zip(x, y):
                f.write(f"{xi:.6f},{yi:.6f}\n")

# =====================
# GUI
# =====================

class RamanMultiwellGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Raman Multiwell Extractor")
        self.geometry("640x230")
        self.resizable(False, False)

        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()

        self._build()

    def _build(self):
        pad = {"padx": 10, "pady": 6}

        tk.Label(self, text="Input LabRAM results file:").grid(
            row=0, column=0, sticky="w", **pad
        )
        tk.Entry(self, textvariable=self.input_file, width=60).grid(
            row=0, column=1, **pad
        )
        tk.Button(self, text="Browse…", command=self.browse_input).grid(
            row=0, column=2, **pad
        )

        tk.Label(self, text="Output folder:").grid(
            row=1, column=0, sticky="w", **pad
        )
        tk.Entry(self, textvariable=self.output_dir, width=60).grid(
            row=1, column=1, **pad
        )
        tk.Button(self, text="Browse…", command=self.browse_output).grid(
            row=1, column=2, **pad
        )

        tk.Button(
            self,
            text="Extract spectra",
            width=20,
            command=self.run
        ).grid(row=2, column=1, pady=15)

        self.status = tk.Label(self, text="", fg="blue")
        self.status.grid(row=3, column=0, columnspan=3, pady=5)

    def browse_input(self):
        file = filedialog.askopenfilename(
            title="Select Raman results file",
            filetypes=[("Text files", "*.txt *.dat"), ("All files", "*.*")]
        )
        if file:
            self.input_file.set(file)

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_dir.set(folder)

    def run(self):
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file.")
            return
        if not self.output_dir.get():
            messagebox.showerror("Error", "Please select an output folder.")
            return

        try:
            self.status.config(text="Processing…")
            self.update_idletasks()

            header, spectra = parse_plate_file(Path(self.input_file.get()))
            write_csv(header, spectra, Path(self.output_dir.get()))

            self.status.config(
                text=f"Done: {len(spectra)} spectra extracted."
            )
            messagebox.showinfo(
                "Complete",
                f"Successfully extracted {len(spectra)} spectra."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="")

# =====================
# Launch GUI
# =====================

if __name__ == "__main__":
    app = RamanMultiwellGUI()
    app.mainloop()

# =====================
# Load spectra
# =====================

def parse_csv(csv_filename):
    data = pd.read_csv(csv_filename, comment='#')

    # parse and load data into spectral objects
    spectral_data = data["Intensity"]
    spectral_axis = data["RamanShift(cm-1)"]

    raman_spectrum = rp.Spectrum(spectral_data, spectral_axis)

    return raman_spectrum