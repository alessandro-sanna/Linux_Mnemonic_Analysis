import pandas as pd
import os

if __name__ == '__main__':
    df = pd.read_csv("elf_dataset_paths.csv", header=0)

    # Check missing samples

    print(df[df["sample_path"] == "None"].shape)

    # Check missing jsons

    print(df[df["json_path"] == "None"].shape)

    