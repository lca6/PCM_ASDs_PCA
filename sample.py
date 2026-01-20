class Sample:
    def __init__(sample, spectrum):

        # from rp.load.labspec
        sample.spectrum = spectrum
        sample.position = "N/A"
        sample.plate = "N/A"
        sample.concentration = "N/A"

    def extract_metadata(sample, filename: str):

        f = filename.removeprefix("to_be_processed/").removesuffix(".txt").split("_")

        for part in f:
            # e.g. A12
            if part[0].isupper():
                sample.position = part

            # e.g. plate1
            if part.startswith("plate"):
                n = part.removeprefix("plate")
                n = int(n)
                sample.plate = n

            # e.g. 60mgml
            if part.endswith("mgml"):
                c = part.removesuffix("mgml")
                c = int(c)
                sample.concentration = c



    def __str__(sample):
        return f"Sample {sample.position} on plate #{sample.plate} at concentration {sample.concentration} mg/mL"
