def data_name_from_path(data_path):
    if data_path is None:
        return None
    data_path_split = data_path.split("\\")
    last = data_path_split[len(data_path_split) - 1]
    last_split = last.split(".")
    data_name = last_split[0]
    return data_name