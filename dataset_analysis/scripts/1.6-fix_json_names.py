import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("./csvs/elf_dataset_paths_polished10.csv", header=0)

    df["json_path"] = df["json_path"].apply(str.replace, args=("elf_virusshare", "elf_virusshare_from_virustotal", 1))

    df.to_csv("./csvs/elf_dataset_paths_polished11.csv")