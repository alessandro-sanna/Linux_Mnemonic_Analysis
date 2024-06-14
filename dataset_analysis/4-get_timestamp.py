import pandas as pd
import swifter
import json
import os


if __name__ == "__main__":
    df = pd.read_csv("~/.mnt/ELF_Dataset/ELF_Dataset_Description.csv.2.3", header=0)
    root_folder = "/home/asanna/.mnt"
    def get_timestamp(jpath):
        jpath = os.path.join(root_folder, jpath)
        with open(jpath) as frJson:
            json_obj = json.load(frJson)
        try:
            ts = json_obj["attributes"]["first_submission_date"]
        except KeyError:
            ts = "None"
        return ts
    
    df["timestamp"] = df["json_path"].swifter.apply(get_timestamp)

    df.to_csv("~/.mnt/ELF_Dataset/ELF_Dataset_Description.csv.3")