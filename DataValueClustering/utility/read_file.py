import glob
import os
import numpy as np


def get_sources_in_experiment_data_directory():
    dir_path = "../experiment_data"
    os.chdir(dir_path)

    res = list()
    for file in glob.glob("*.txt"):
        filename = file.replace(".txt", "")
        res.append([filename, lambda path=file: read_data_values_from_file(dir_path + "\\" + path)])
    return np.array(res)


def read_data_values_from_file(path):
    with open(path, encoding='UTF-8') as f:
        values = f.read().splitlines()
    assert len(values) > 0
    return values


if __name__ == '__main__':
    print(get_sources_in_experiment_data_directory())
