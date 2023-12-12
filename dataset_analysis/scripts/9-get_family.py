import pandas as pd
import os


if __name__ == '__main__':
    df = pd.read_csv("./csvs/elf_dataset_paths_polished12.csv", header=0)

    avclass_results = './csvs/avclass_results3.txt'
    with open(avclass_results) as frTxt:
        avclass_lines = \
            [x.strip().split() for x in frTxt.readlines()]
    
    df["AVClass_Family"] = "Not Found"
    l = len(avclass_lines)
    for i, x in enumerate(avclass_lines):
        print(f"\r{i}/{l}", end='')
        
        try:
            sha256_hash = x[0]
            family = x[1]
        except IndexError:
            print(x)

        try:
            df.loc[df['sha256_hash'] == sha256_hash, "AVClass_Family"] = family
        except:
            continue
    
    df = df[df.columns[~df.columns.str.startswith('Unnamed')]]
    df.to_csv("./csvs/elf_dataset_paths_polished13.csv")
        
