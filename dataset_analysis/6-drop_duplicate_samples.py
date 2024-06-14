import pandas as pd
import swifter
import json
import os

if __name__ == '__main__':
    df = pd.read_csv("./csvs/elf_dataset_paths_polished3.csv", header=0)
    root_folder = "/home/asanna/.mnt"
    def get_sha256_hash(h, jpath):
        jpath = os.path.join(root_folder, jpath)
        with open(jpath) as frJson:
            json_obj = json.load(frJson)
        try:
            nh = json_obj["attributes"]["sha256"]
        except KeyError:
            nh = h
        return nh
    
    df["sha256_hash"] = df.swifter.apply(lambda x: \
                            get_sha256_hash(x["sha256_hash"],
                                            x["json_path"]),
                                        axis=1)

    df = df.drop_duplicates("sha256_hash")
    df.to_csv("./csvs/elf_dataset_paths_polished4.csv")
