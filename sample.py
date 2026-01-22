from filter import processing_folder

class Sample:
    def __init__(self):

        self.well = "N/A"
        self.drug = "PCM"
        self.polymer = "N/A"
        self.row = "N/A"

        self.col = 0
        self.plate = 0
        self.concentration = 0
        self.drug_loading = 0
        self.polymer_loading = 0


    def get_sample_metadata(self, filename: str, spectrum):

        # from rp.load.labspec
        self.spectrum = spectrum

        file = filename.removeprefix(f"{processing_folder}/").removesuffix(".txt").split("_")

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

        # TODO
        match self.plate:
            case 1:
                ...
            case 2:
                ...
            case 3:
                ...
            case 4:
                ...

    def __str__(self):
        return f"Sample {self.well} on plate #{self.plate} at concentration {self.concentration} mg/mL"