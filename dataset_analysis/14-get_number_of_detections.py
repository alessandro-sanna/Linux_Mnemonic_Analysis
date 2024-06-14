import pandas as pd
import swifter
import json
import os

if __name__ == '__main__':
    df = pd.read_csv("./csvs/elf_dataset_paths_polished13.csv", header=0)
    root_folder = "/home/asanna/.mnt"
    def get_number_of_detections(jpath):
        jpath = os.path.join(root_folder, jpath)
        with open(jpath) as frJson:
            json_obj = json.load(frJson)
        try:
            nh = json_obj["attributes"]["last_analysis_stats"]
            mal = nh["malicious"]
            und = nh["undetected"]
        except KeyError:
            mal = -1
            und = -1
        return mal, und
    
    df[["number_of_malicious", "number_of_undetected"]] = \
        df["json_path"].swifter.apply(
            lambda x: pd.Series(get_number_of_detections(x)))

    df.to_csv("./csvs/elf_dataset_paths_polished14.csv")
