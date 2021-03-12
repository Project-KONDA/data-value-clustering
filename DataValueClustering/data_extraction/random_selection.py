import random

from data_extraction import read_data_values_from_file


def get_random_values(data_path, n):
    data = read_data_values_from_file(data_path)
    min = 0
    max = len(data)-1
    selected_values = []
    indices = []
    for i in range(n):
        r = random.randint(min, max)
        while r in indices:
            r = random.randint(min, max)
        v = data[r]
        selected_values.append(v)
        indices.append(r)
    return selected_values


if __name__ == "__main__":
    print(get_random_values("../data/midas_dates.txt", 5))