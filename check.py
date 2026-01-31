import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ramanspy as rp
import sys

from parse import parse
from sample import Sample

from settings import MACBOOK_URL, PCA_OUTPUT

def main():
    # Parse any multiwell files in the analyse/ folder
    parsed_files, _ = parse()

    # Save parsed_files to txt file
    with open(f"{PCA_OUTPUT}/parsed_files.txt", "w") as f:
        json.dump(parsed_files, f)

    dataframes_2_and_3 = []
    dataframe_4 = []
    dicts = []

    for file in parsed_files:

        spectrum = rp.load.labspec(f"{MACBOOK_URL}{file}")

        sample = Sample(file, spectrum)

        with open(f"{MACBOOK_URL}{file}") as f:

            l = []
            for line in f:
                if line[0] != "#":
                    shift, intensity = line.split("\t", maxsplit=1)

                    shift = float(shift)
                    intensity = float(intensity[:-1])

                    l.append(
                        dict(
                            sample=sample,
                            shift=shift,
                            intensity=intensity,
                        )
                    )

            df = pd.DataFrame(l)
            df = df.pivot(index="sample", columns="shift", values="intensity")

            if sample.plate == 4:
                dataframe_4.append(df)
            elif sample.plate in [2, 3]:
                dataframes_2_and_3.append(df)


    plates_2_and_3 = pd.concat(dataframes_2_and_3)
    plate_4 = pd.concat(dataframe_4)

    diff_between_plates = compare(plates_2_and_3.columns, plate_4.columns)

    x = range(len(diff_between_plates))
    y = diff_between_plates.values

    plt.figure(figsize=(6, 4))
    plt.plot(x, y, marker='o', linestyle='-')
    plt.xlabel("Sample number")
    plt.ylabel("Shift difference")
    plt.title("Shift difference between plate 4 and plates 2 and 3")
    plt.ylim(0, 0.1)
    plt.grid(True)
    plt.savefig("difference_between_plate4_and_plates_2_and_3.png", format="png", bbox_inches="tight", dpi=300)
    plt.show()


def compare(index1, index2):

    if len(index1) != len(index2):
        sys.exit("Both indices must be of the same length")

    diff = pd.Index(np.abs(index1.values - index2.values))

    return diff


if __name__ == "__main__":
    main()