import pandas as pd
import swifter
import os
import subprocess


if __name__ == '__main__':
    csv_path = "/home/asanna/.mnt/ELF_Dataset/unpacked/elf_to_2022.csv"
    df = pd.read_csv(csv_path, header=0)

    r_path = "/home/asanna/.mnt/ELF_Dataset/unpacked"
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
        df["file_path"].swifter.apply(
            lambda x: pd.Series(get_packing_info(x)))
    df = df[df.columns[~df.columns.str.startswith('Unnamed')]]
    df.to_csv(csv_path.replace("elf_to_2022", "elf_to_2022_pinfo.1.csv"))