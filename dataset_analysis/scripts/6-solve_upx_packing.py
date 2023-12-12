import pandas as pd
import swifter
import os
import subprocess


if __name__ == '__main__':
    df = pd.read_csv("./csvs/elf_dataset_paths_polished5.csv", header=0)

    r_path = "/home/asanna/.mnt"
    def solve_upx_packing(s_is_packed, s_source, s_path):
        if not s_is_packed:
            return -1, "None"
        else:
            o_root = os.path.join(r_path, "ELF_Dataset", s_source, "UPX_depacked")
            
            s_path = os.path.join(r_path, s_path)
            o_path = os.path.join(o_root, "UPX_DEPACKED-" + os.path.basename(s_path))
            try:
                command = f"upx -d {s_path} -o{o_path}"
                subprocess.check_output(command.split())
            except subprocess.CalledProcessError as exc:
                error_code = exc.returncode
                unpacked_path = "None"
            else:
                error_code = 0
                unpacked_path = o_path
            finally:
                return error_code, unpacked_path

    df[["UPX-d_error_code", "UPX-d_output_path"]] = \
        df.swifter.apply(
            lambda x: pd.Series(
                solve_upx_packing(
                    x["is_packed"], x["source"], x["sample_path"])),
            axis=1)
    
    df = df[df.columns[~df.columns.str.startswith('Unnamed')]]
    df.to_csv("./csvs/elf_dataset_paths_polished6.csv")