import pandas as pd
import swifter
import os
import subprocess


if __name__ == '__main__':
    name = "~/.mnt/ELF_Dataset/ELF_Dataset_Description.csv"
    df = pd.read_csv(name, header=0)
    # df = df.head(10)
    r_path = "/home/asanna/.mnt"

    def get_architecture_with_readelf(s_path):
        s_path = os.path.join(r_path, s_path)
        try:
            command = f"readelf -h {s_path}"
            s_output = str(subprocess.check_output(command.split()), encoding="ascii")
            s_output = [x for x in s_output.splitlines() if x.strip().startswith("Machine:")][0]
            return s_output.replace("Machine:", "").strip()
        except Exception as exc:
            return exc.__class__

    df[["ReadELF_architecture"]] = \
        df["sample_path"].swifter.apply(
            lambda x: pd.Series(get_architecture_with_readelf(x)))
    
    df = df[df.columns[~df.columns.str.startswith('Unnamed')]]
    df.to_csv(name+".2")