import pandas as pd
import os
import swifter
import json


if __name__ == '__main__':
    df = pd.read_csv("./csvs/elf_dataset_paths_polished12.csv", header=0)
    ndjson_path = "./csvs/data_for_avclass2.ndjson"
    r_path = "/home/asanna/.mnt"

    # df = df.head(10)
    l = df.shape[0]

    for i, row in enumerate(df.iterrows()):
        j_path = row[1]["json_path"]
        j_path = os.path.join(r_path, j_path)
        with open(j_path) as frJson, open(ndjson_path, "a") as faNdjson:
            json.dump(json.load(frJson), faNdjson)
            faNdjson.write('\n')
        print(f"\r{i+1}/{l}", end='')

    # avclass -hash sha256 -stats ndjson_file
    
