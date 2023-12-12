import subprocess
import pandas as pd
import swifter
import os
import tempfile
from copy import deepcopy
import shutil
import sys


if __name__ == '__main__':
    csv_name = sys.argv[1]
    ghidra_script = sys.argv[2]
    noah_mnt = "/home/asanna/.mnt"
    root_folder = "/home/asanna/Development/DIMVA_Linux_Malware/experiments"
    df_name = os.path.join(csv_name)
    df = pd.read_csv(df_name, header=0)
    command_prototype =  f"{root_folder}/ghidra_10.4_PUBLIC/support/analyzeHeadless <project_directory> <project_name> -import <program_to_analyze> -postscript <path_to_script.py>"
    project_base_folder = f"{root_folder}/ProjectBaseState/"
    

    def analyzeSample(s_path):
        # Build Command
        temp_folder = tempfile.TemporaryDirectory()
        temp_sample = tempfile.NamedTemporaryFile()
        # s_path = os.path.join(noah_mnt, s_path)
        shutil.copy2(s_path, temp_sample.name)
        command = deepcopy(command_prototype)
        command = command.replace("<path_to_script.py>", ghidra_script)
        command = command.replace("<project_directory>", temp_folder.name)
        shutil.copytree(project_base_folder, temp_folder.name, dirs_exist_ok=True)
        command = command.replace("<project_name>", "Project")
        command = command.replace("<program_to_analyze>", temp_sample.name)
        
        # Run Command
        _ = subprocess.check_output(command.split())
        
    
    df_series = df["sample_path"].swifter.apply(lambda x: os.path.join(noah_mnt, x))
    df_series.swifter.apply(analyzeSample)
        
    