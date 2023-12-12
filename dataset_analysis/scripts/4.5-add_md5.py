import pandas as pd
import swifter
import json
import os

if __name__ == '__main__':
    df = pd.read_csv("./csvs/elf_dataset_paths_polished11.csv", header=0)
    root_folder = "/home/asanna/.mnt"
    def get_md5_hash(jpath):
        jpath = os.path.join(root_folder, jpath)
        try:
            with open(jpath) as frJson:
                json_obj = json.load(frJson)
        except FileNotFoundError:
            with open(jpath.replace("_from_virustotal", "", 1)) as frJson:
                json_obj = json.load(frJson)
        try:
            nh = json_obj["attributes"]["md5"]
        except KeyError:
            nh = "-1"
        return nh
    
    df["md5_hash"] = df["json_path"].swifter.apply(get_md5_hash)

    df = df.drop_duplicates("sha256_hash")
    df.to_csv("./csvs/elf_dataset_paths_polished12.csv")
