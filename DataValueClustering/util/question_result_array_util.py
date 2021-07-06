import numpy as np


def get_array_part(selectables, question_array, answers):
    '''
    select part of array based on answers to a binary questinaire
    selectables must be array with list of indices of answers with positive dependencies in column 0 and with negative dependencies in column 1
    '''
    assert (len(answers) == len(question_array))
    result = list()
    for line in selectables:
        apply = True
        for dep in line[0]:  # check positive dependencies
            apply = apply and answers[dep]
        for not_dep in line[1]:  # check negative dependencies
            apply = apply and not (answers[not_dep])
        if apply:
            result.append(line[2:])
    return np.array(result, dtype=object)