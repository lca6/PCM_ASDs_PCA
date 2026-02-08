from pcm_asds_pca.config.settings import ANALYSIS_FOLDER

plate1 = {
    "polymer": {
        1: "PLS",
        2: "PLS",
        3: "PLS",
        4: "SOL",
        5: "SOL",
        6: "SOL",
        7: "AFF",
        8: "AFF",
        9: "AFF",
        10: "HPMCAS",
        11: "HPMCAS",
        12: "HPMCAS",
    },
    "drug_loading": {
        "A": 95,
        "B": 90,
        "C": 85,
        "D": 80,
        "E": 75,
        "F": 70,
        "G": 60,
        "H": 50,
    },
}

plate2 = {
    "polymer": {
        1: "PLS",
        2: "PLS",
        3: "PLS",
        4: "AFF",
        5: "AFF",
        6: "AFF",
        7: "PLS",
        8: "PLS",
        9: "PLS",
        10: "AFF",
        11: "AFF",
        12: "AFF",
    },
    "drug_loading": {
        "A": 100,
        "B": 95,
        "C": 90,
        "D": 85,
        "E": 80,
        "F": 75,
        "G": 70,
        "H": 0,
    },
}

plate3 = {
    "polymer": {
        1: "PLS",
        2: "PLS",
        3: "PLS",
        4: "AFF",
        5: "AFF",
        6: "AFF",
        7: "HPMCAS",
        8: "HPMCAS",
        9: "HPMCAS",
        10: "SOL",
        11: "SOL",
        12: "SOL",
    },
    "drug_loading": {
        "A": 100,
        "B": 95,
        "C": 90,
        "D": 85,
        "E": 80,
        "F": 75,
        "G": 70,
        "H": 0,
    },
}

plate4 = {
    "polymer": {
        1: "PLS",
        2: "PLS",
        3: "PLS",
        4: "AFF",
        5: "AFF",
        6: "AFF",
        7: "HPMCAS",
        8: "HPMCAS",
        9: "HPMCAS",
        10: "SOL",
        11: "SOL",
        12: "SOL",
    },
    "drug_loading": {
        "A": 100,
        "B": 95,
        "C": 90,
        "D": 85,
        "E": 80,
        "F": 75,
        "G": 70,
        "H": 0,
    },
}


plate2_crystalline_wells = [
    "A3",
    "A10",
    "A11",
    "A12",
    "B1",
    "B4",
    "B5",
    "B6",
    "B7",
    "B9",
    "B10",
    "B11",
    "C4",
    "C5",
    "C6",
    "C7",
    "C9",
    "C10",
    "C11",
    "C12",
    "D4",
    "D5",
    "D6",
    "D10",
    "D12",
    "E9",
    "E10",
    "E11",
    "E12",
]

plate3_crystalline_wells = [
    "A2",
    "A3",
    "A4",
    "A6",
    "A7",
    "A8",
    "A9",
    "A10",
    "A11",
    "A12",
    "B1",
    "B2",
    "B3",
    "B5",
    "B6",
    "B7",
    "B8",
    "B9",
    "B10",
    "B11",
    "B12",
    "C1",
    "C3",
    "C6",
    "C7",
    "C8",
    "C9",
    "C10",
    "C11",
    "C12",
    "D1",
    "D3",
    "D4",
    "D6",
    "D7",
    "D8",
    "D9",
    "D10",
    "D11",
    "D12",
    "E1",
    "E2",
    "E3",
    "E7",
    "E8",
    "E9",
    "E10",
    "E12",
    "F3",
    "F7",
    "F8",
    "F9",
    "F10",
    "F11",
    "F12",
    "G10",
    "G11",
]

plate4_crystalline_wells = [
    "A1",
    "A4",
    "A5",
    "A6",
    "A8",
    "A10",
    "B1",
    "B2",
    "B3",
    "B5",
    "B6",
    "B8",
    "B9",
    "B10",
    "B12",
    "C1",
    "C2",
    "C4",
    "C5",
    "C6",
    "C8",
    "C10",
    "C12",
    "D2",
    "D6",
    "D7",
    "D12",
    "E2",
    "E4",
    "E5",
    "E6",
    "E7",
    "E8",
    "E10",
    "F4",
    "F5",
    "F6",
    "F9",
    "F10",
    "F12",
    "G1",
    "G4",
    "G5",
    "G6",
    "G9",
    "G10",
    "G11",
]


class Sample:

    def __init__(self, filename: str, spectrum):

        self.appearance = "amorphous"
        self.position = "centre"
        self.drug = "PCM"
        self.well = "N/A"
        self.polymer = "N/A"
        self.row = "N/A"

        self.col = 0
        self.plate = 0
        self.concentration = 0
        self.drug_loading = 0
        self.polymer_loading = 0

        # from rp.load.labspec
        self.spectrum = spectrum

        file = filename.removeprefix(f"{ANALYSIS_FOLDER}/").removesuffix(".txt")

        if file == "glass_reference":
            self.drug = "N/A"
            self.well = "Glass"
            return

        for part in file.split("_"):
            # e.g. A12
            if part[0].isupper():
                self.well = part
                self.row = part[0]
                self.col = int(self.well[1:])

            # e.g. plate1
            if part.startswith("plate"):
                n = part.removeprefix("plate")
                n = int(n)
                self.plate = n

            # e.g. 60mgml
            if part.endswith("mgml"):
                c = part.removesuffix("mgml")
                c = int(c)
                self.concentration = c

            if part == "edge":
                self.position = "Edge"

        # Assign polymer, drug loading, and polymer loading to each sample
        match self.plate:

            case 1:
                self.polymer = plate1["polymer"][self.col]
                self.drug_loading = plate1["drug_loading"][self.row]
                self.polymer_loading = 100 - self.drug_loading

            case 2:
                self.polymer = plate2["polymer"][self.col]
                self.drug_loading = plate2["drug_loading"][self.row]
                self.polymer_loading = 100 - self.drug_loading
                if self.well in plate2_crystalline_wells:
                    self.appearance = "crystalline"

            case 3:
                self.polymer = plate3["polymer"][self.col]
                self.drug_loading = plate3["drug_loading"][self.row]
                self.polymer_loading = 100 - self.drug_loading
                if self.well in plate3_crystalline_wells:
                    self.appearance = "crystalline"

            case 4:
                self.polymer = plate4["polymer"][self.col]
                self.drug_loading = plate4["drug_loading"][self.row]
                self.polymer_loading = 100 - self.drug_loading
                if self.well in plate4_crystalline_wells:
                    self.appearance = "crystalline"

    def __str__(self):
        if self.well == "Glass":
            return "Glass reference"
        else:
            return f"Sample {self.well} ({self.position}) on plate #{self.plate} at concentration {self.concentration} mg/mL {self.drug}/{self.polymer} {self.drug_loading}%/{self.polymer_loading}% {self.appearance}"
