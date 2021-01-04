def remove_duplicates(values):
    result = list(dict.fromkeys(values))
    assert len(result) <= len(values)
    return result
