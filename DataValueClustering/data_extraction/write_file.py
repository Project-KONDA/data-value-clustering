
def write_data_values_to_file(path, values):
    with open(path, "w", encoding='UTF-8') as f:
        for item in values:
            f.write("%s\n" % item)
    f.close()