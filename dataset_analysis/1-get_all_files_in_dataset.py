import os
import pandas as pd
import glob


if __name__ == '__main__':
    rpath = "/home/asanna/.mnt/ELF_Dataset/"

    af_path = "./csvs/all_files.csv"
    if not os.path.exists(af_path):
        all_files = [x for x in 
                        glob.glob(os.path.join(rpath, "**", "*"), recursive=True)
                        if os.path.isfile(x)]

        with open(af_path, "w") as fwCsv:
            for f in all_files:
                fwCsv.write(f.replace("/home/asanna/.mnt/", "") + "\n")
    else:
        with open(af_path) as frCsv:
            all_files = [x.strip() for x in frCsv.readlines()]

    print("Done!")

    all_jsons = [x for x in all_files
                 if x.endswith(".json")]
    
    all_samples = [x for x in all_files
                   if not x.endswith(".json")]
    
    def l_names(l):
        return [os.path.splitext(os.path.basename(s))[0] for s in l]
    
    aj_names, as_names = l_names(all_jsons), l_names(all_samples)

    as_names = [x.replace("VirusShare_", "") for x in as_names]

    l_j, l_s = len(all_jsons), len(all_samples)
    
    to_df = list()
    
    
    for i_j, j in enumerate(aj_names):
        if j in as_names:
            to_df.append([
                j,
                all_jsons[i_j],
                all_samples[as_names.index(j)]
            ])
    #     else:
    #         to_df.append([
    #             j,
    #             all_jsons[i_j],
    #             "None"
    #         ])
        print(f"\rScanning JSONS: {i_j + 1} / {l_j}...", end="")

    # for i_s, s in enumerate(as_names):
    #     if s not in aj_names:
    #         to_df.append([
    #             s,
    #             "None",
    #             all_samples[i_s]
    #         ])
    #     print(f"\rScanning Samples: {i_s + 1} / {l_s}...", end="")
    
    df = pd.DataFrame(to_df, columns=[
        "sha256_hash",
        "json_path",
        "sample_path"
    ])

    df.to_csv("./csvs/elf_dataset_paths_polished.csv")