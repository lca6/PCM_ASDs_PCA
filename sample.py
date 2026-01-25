from filter import ANALYSIS_FOLDER

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


class Sample:
    def __init__(self, filename: str, spectrum):

        self.well = "N/A"
        self.drug = "PCM"
        self.polymer = "N/A"
        self.row = "N/A"

        self.col = 0
        self.plate = 0
        self.concentration = 0
        self.drug_loading = 0
        self.polymer_loading = 0

        # from rp.load.labspec
        self.spectrum = spectrum

        file = (
            filename.removeprefix(f"{ANALYSIS_FOLDER}/").removesuffix(".txt").split("_")
        )

        for part in file:
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

            case 3:
                self.polymer = plate3["polymer"][self.col]
                self.drug_loading = plate3["drug_loading"][self.row]
                self.polymer_loading = 100 - self.drug_loading

            case 4:
                self.polymer = plate4["polymer"][self.col]
                self.drug_loading = plate4["drug_loading"][self.row]
                self.polymer_loading = 100 - self.drug_loading

    def __str__(self):
        return f"Sample {self.well} on plate #{self.plate} at concentration {self.concentration} mg/mL {self.drug}/{self.polymer} {self.drug_loading}%/{self.polymer_loading}% "
