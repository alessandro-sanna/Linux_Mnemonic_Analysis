import pandas as pd
import swifter
import os
import subprocess


if __name__ == '__main__':
    df = pd.read_csv("./csvs/elf_dataset_paths_polished6.csv", header=0)
    # df = df.head(10)
    r_path = "/home/asanna/.mnt"

    def get_sample_info(s_path):
        s_path = os.path.join(r_path, s_path)
        try:
            command = f"file {s_path}"
            s_output = str(subprocess.check_output(command.split()), encoding="ascii")
            _, output = s_output.split(':')
            fields = output.split(',')
            endianess = fields[0].split()[2]
            bits_of_addresses = fields[0].split()[1]
            architecture = fields[1]
            architecture_info = fields[2]
            static_or_dynamic = \
                "Static" if "statically" in s_output else "Dynamic"
            stripped = \
                True if "stripped" in s_output and "not stripped" in s_output else False
            return [x.strip() if type(x) == str else x for x in 
                    [endianess, bits_of_addresses, architecture,
                    architecture_info, static_or_dynamic, stripped]]
        except:
            return ["ERROR"] * 6

    df[["endianess", "bits_of_addresses", "architecture",
        "architecture_info", "static_or_dynamic", "stripped"]] = \
        df["sample_path"].swifter.apply(
            lambda x: pd.Series(get_sample_info(x)))
    
    df = df[df.columns[~df.columns.str.startswith('Unnamed')]]
    df.to_csv("./csvs/elf_dataset_paths_polished7.csv")