from random import shuffle

from data_extraction import read_data_values_from_file
from data_extraction.write_file import write_data_values_to_file


def shuffle_values(path):
    path_without_ending = path[0:len(path)-4]
    values = read_data_values_from_file(path)
    shuffle(values)
    write_data_values_to_file(path_without_ending+"_randomized.txt", values)

if __name__ == "__main__":
    shuffle_values("../data/midas_dates.txt")