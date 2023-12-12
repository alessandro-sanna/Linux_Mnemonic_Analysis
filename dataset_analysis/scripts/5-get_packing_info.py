import pandas as pd
import swifter
import os
import subprocess


if __name__ == '__main__':
    df = pd.read_csv("./csvs/elf_dataset_paths_polished4.csv", header=0)

    r_path = "/home/asanna/.mnt"
    def get_packing_info(s_path):
        try:
            s_path = os.path.join(r_path, s_path)
            is_packed = str(subprocess.check_output(
                f"bintropy {s_path}".split()
            ), encoding="ascii").strip()
            highest_entropy, average_entropy = \
                str(subprocess.check_output(
                    f"bintropy --do-not-decide {s_path}".split()
                ), encoding="ascii").split()
            return [is_packed, highest_entropy, average_entropy]
        except:
            return ["ERROR"] * 3

    df[["is_packed", "max_entropy", "avg_entropy"]] = \
        df["sample_path"].swifter.apply(
            lambda x: pd.Series(get_packing_info(x)))
    df = df[df.columns[~df.columns.str.startswith('Unnamed')]]
    df.to_csv("./csvs/elf_dataset_paths_polished5.csv")