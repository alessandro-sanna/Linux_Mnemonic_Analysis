import pandas as pd
import glob


if __name__ == '__main__':
    df = pd.read_csv("/home/asanna/.mnt/ELF_Dataset/unpacked/elf_to_2022.csv")
    all_encs = glob.glob("/home/asanna/.mnt/ELF_Dataset/encodings_benign_final/**/*", recursive=True)

    df["has_encoding"] = df.apply(lambda x: f"/home/asanna/.mnt/ELF_Dataset/encodings_benign_final/{x['sha256_hash']}.csv" in all_encs, axis=1)

    df.to_csv("filtered_elf_to_2022.csv")