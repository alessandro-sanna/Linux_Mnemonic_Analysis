from re import sub

from pandas import concat, read_csv, read_pickle


def prepare(x, name):
    """
        Merge together the benign and malicious datasets and create a dataset suitable for good old ML.
    """
    malicious_info = read_csv("malicious_info.csv")

    malicious_info = malicious_info[malicious_info["sha256_hash"].isin(x)]
    malicious_asm = read_csv("malicious_asm.csv")
    malicious = malicious_info.merge(right=malicious_asm, left_on="sha256_hash", right_on="hashes")

    family = malicious["AVClass_Family"]
    architecture = malicious["architecture"]
    abi = malicious["architecture_info"]
    family = [sub(r"SINGLETON:.*", "singleton", i) for i in family]
    to_delete = ['Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0_x', 'sha256_hash', 'json_path',
                 'sample_path', 'source', 'timestamp', 'is_packed', 'max_entropy', 'avg_entropy',
                 'UPX-d_error_code', 'UPX-d_output_path', 'endianess', 'bits_of_addresses',
                 'architecture', 'architecture_info', 'static_or_dynamic', 'stripped', 'AVClass_Family',
                 'number_of_malicious', 'number_of_undetected', 'md5_hash', 'ReadELF_architecture',
                 'ReadELF_class', 'year', 'Unnamed: 0_y', 'hashes']
    malicious = malicious.drop(labels=to_delete, axis=1)
    malicious["malicious"] = True
    malicious["family"] = family
    malicious["architecture"] = architecture
    malicious["abi"] = abi
    print(f"malicious: {len(malicious)}")

    benign_info = read_csv("benign_info.csv")
    benign_info = benign_info[benign_info["sha256_hash"].isin(x)]

    benign_asm = read_csv("benign_asm.csv")
    benign = benign_info.merge(right=benign_asm, left_on="sha256_hash", right_on="hashes")

    abi = benign["architecture_info"]
    to_delete = ['Unnamed: 0_x', 'file_path', 'sha256_hash', 'ls_date', 'ls_year', 'is_packed',
                 'max_entropy', 'avg_entropy', 'endianess', 'bits_of_addresses', 'architecture',
                 'architecture_info', 'static_or_dynamic', 'stripped', 'Unnamed: 0_y', 'hashes']
    benign = benign.drop(labels=to_delete, axis=1)
    benign["malicious"] = False
    benign["family"] = "benign"
    benign["architecture"] = "?"
    benign["abi"] = "?"
    benign["abi"] = abi
    print(f"benign: {len(benign)}")

    malicious_features = set(malicious.columns.to_list())
    benign_features = set(benign.columns.to_list())
    data_set = concat([malicious, benign])
    data_set = data_set[sorted(list(malicious_features & benign_features))]
    print(f"samples: {len(data_set)}")

    data_set.to_feather(f"{name}.feather")

    print("done")

    return data_set


with open("time.pkl", "rb") as f:
    x_train, x_test, y_train, y_test = read_pickle(f)

train_set = prepare(x_train, "train")
test_set = prepare(x_test, "test")

d = concat([train_set, test_set])
d.to_feather("data.feather")
