def read_data_values_from_file(path):
    with open(path, encoding='UTF-8') as f:
        values = f.read().splitlines()
    assert len(values) > 0
    return values