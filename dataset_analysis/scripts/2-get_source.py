import pandas as pd


if __name__ == "__main__":
    df = pd.read_csv("./csvs/elf_dataset_paths_polished.csv", header=0)

    df["source"] = df["json_path"].apply(lambda x: x.split('/')[1])

    df.to_csv("./csvs/elf_dataset_paths_polished2.csv")