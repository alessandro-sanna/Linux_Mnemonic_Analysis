import os
import json
import pandas as pd


if __name__ == '__main__':
    encs_mnt = "/home/asanna/.mnt/ELF_Dataset/encodingsBenignBatch"
    
    files = [os.path.join(encs_mnt, x) for x in os.listdir(encs_mnt)]
    num_files = len(files)
    res_dict = {"hashes": list()}

    for i, f in enumerate(files):
        h = os.path.basename(f).replace(".csv", "")
        res_dict["hashes"].append(h)
        with open(f) as frCsv:
            while line := frCsv.readline():
                line = line.strip()
                if line not in res_dict.keys():
                    res_dict.update({line: [0]*(num_files)})
                res_dict[line][i] += 1
        print(f"\r{i + 1}/{num_files}", end='')

    json_name = "resDict_benign.json"
    with open(json_name, "w") as frJson:
        json.dump(res_dict, frJson, indent=4)
    
    df = pd.read_json(json_name)
    df.to_csv(json_name.replace("Dict", "_df").replace(".json", ".csv"))

    
