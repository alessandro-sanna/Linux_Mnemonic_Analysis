import subprocess
import pandas as pd
import swifter
import os
import tempfile
from copy import deepcopy
import shutil
import sys

import pandas as pd
import multiprocessing

# Funzione che verrà applicata a ciascun sottoinsieme


if __name__ == '__main__':
    csv_name = sys.argv[1]
    ghidra_script = sys.argv[2]
    noah_mnt = "/home/asanna/.mnt/ELF_Dataset/unpacked"
    root_folder = "/home/asanna/Development/DIMVA_Linux_Malware/experiments"
    # df_name = os.path.join(csv_name)
    df = pd.read_csv(csv_name, header=0)

    # df = df.head(100)
    command_prototype =  f"{root_folder}/ghidra_10.4_PUBLIC/support/analyzeHeadless <project_directory> <project_name> -import <program_to_analyze> -postscript <path_to_script.py>"
    project_base_folder = f"{root_folder}/ProjectBaseState/"
    output_folder = sys.argv[3]
    csv_fielf = sys.argv[4]
    

    def analyzeSample(s_path, sha256_hash, o_folder):
        o_file = os.path.join(o_folder, sha256_hash + ".csv")
        if os.path.exists(o_file):
            pass
        else:
            # Build Command
            temp_folder = tempfile.TemporaryDirectory()
            temp_sample = tempfile.NamedTemporaryFile()
            s_path = os.path.join(noah_mnt, s_path)
            shutil.copy2(s_path, temp_sample.name)
            command = deepcopy(command_prototype)
            command = command.replace("<path_to_script.py>", ghidra_script)
            command = command.replace("<project_directory>", temp_folder.name)
            shutil.copytree(project_base_folder, temp_folder.name, dirs_exist_ok=True)
            command = command.replace("<project_name>", "Project")
            command = command.replace("<program_to_analyze>", temp_sample.name)
            
            # Run Command
            _ = subprocess.check_output(command.split())
        
    def process_dataframe(sub_df):
        # Esempio di operazione: restituisci la somma delle colonne
        # df_series = sub_df["file_path"].swifter.apply(lambda x: os.path.join(noah_mnt, x))
        # df_series.swifter.apply(analyzeSample)

        sub_df.swifter.apply(lambda x: analyzeSample(x["file_path"], x["sha256_hash"], output_folder), axis=1)

    # Esempio di DataFrame

    n_processes = 50
    df["o_file"] = df["sha256_hash"].swifter.apply(lambda x: os.path.join(output_folder, x + ".csv"))
    df = df[~df["o_file"].apply(lambda x: os.path.exists(x) and os.stat(x).st_size != 0)]
    # Dividi il DataFrame in 10 sottoinsiemi
    sottoinsiemi = [df.iloc[i:i+int(len(df)/n_processes)] for i in range(0, len(df), int(len(df)/n_processes))]

    # Funzione per elaborare i sottoinsiemi in parallelo
    def multiprocessing_apply(data):
        pool = multiprocessing.Pool(processes=n_processes)  # Numero di processi desiderati
        results = pool.map(process_dataframe, data)
        pool.close()
        pool.join()
        return results

    # Esegui l'elaborazione in parallelo sui sottoinsiemi
    risultati = multiprocessing_apply(sottoinsiemi)

    # print(risultati)
        
    
    # df_series = df["sample_path"].swifter.apply(lambda x: os.path.join(noah_mnt, x))
    # df_series.swifter.apply(analyzeSample)
        
    