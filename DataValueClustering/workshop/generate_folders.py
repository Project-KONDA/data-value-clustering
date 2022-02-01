import os
import re
import shutil

path_targetFolder = "./workshop_clustering_tool"

path_slides = "workshop_files/Folien_KONDA_Workshop_Clustering.pdf"
path_alias_Table = "AliasQuestionarireInput.xlsx"
path_alias_Table2 = "./workshop_files/Alias1.xlsx"

path_InstructionA1 = "./workshop_files/Anleitung_GruppeA1.pdf"
path_InstructionB1 = "./workshop_files/Anleitung_GruppeB1.pdf"
path_InstructionA2 = "./workshop_files/Anleitung_GruppeA2.pdf"
path_InstructionB2 = "./workshop_files/Anleitung_GruppeB2.pdf"

# path_InstructionA1 = "./workshop_files/Anleitung_Gruppe_A1_Pilot.pdf"
# path_InstructionB1 = "./workshop_files/Anleitung_Gruppe_B1_Pilot.pdf"
# path_InstructionA2 = "./workshop_files/Anleitung_Gruppe_A2_Pilot.pdf"
# path_InstructionB2 = "./workshop_files/Anleitung_Gruppe_B2_Pilot.pdf"

path_Werteliste_A = "./workshop_files/RepositoryName_Werteliste.xlsx"
path_Werteliste_B = "./workshop_files/ActorName_Werteliste.xlsx"
# path_Werteliste_C = "./workshop_files/RepositoryLocationName_Werteliste.xlsx"

# alias_file_name = "alias_pilot.txt"
# alias_pairs_file_name = "alias_pairs_pilot.txt"
alias_file_name = "alias.txt"
alias_pairs_file_name = "alias_pairs.txt"

SEPARATOR = "|"


def generateGroups():
    alias_list = readAliasList(path_alias_Table)
    print(alias_list)
    if alias_list is None:
        return

    groups = ("A1", "B2", "A2", "B1")
    division = list()

    for i, alias in enumerate(alias_list):
        t = (alias, groups[i % 4], i // 2)
        division.append(t)

    textfile = open(alias_file_name, "w")
    for i, element in enumerate(division):
        textfile.write(element[0] + SEPARATOR + element[1] + SEPARATOR + str(element[2]) + "\n")
    textfile.close()
    textfile2 = open(alias_pairs_file_name, "w")
    for i in range(len(division)//2):
        assert (division[i * 2][2] == division[i * 2 + 1][2])
        textfile2.write(division[i * 2][0] + SEPARATOR + division[i * 2 + 1][0] + "\n")
        textfile2.write(division[i * 2 + 1][0] + SEPARATOR + division[i * 2][0] + "\n")
    if len(division) % 2 == 1:
        textfile2.write(division[len(division)-1][0])
    textfile2.close()

    try:
        os.mkdir(path_targetFolder)
    except FileExistsError:
        pass

    for tupel in division:
        generateFolder(tupel)


def readAliasList(path):
    import collections
    import pandas as pd
    import random
    from tkinter import messagebox

    df = pd.read_excel(path_alias_Table, sheet_name=0, header=0)
    list_from_table = df[df.columns[1]].tolist()
    list_from_table_answers = df[df.columns[2]].tolist()

    result_list_noDemo = []
    result_list = []
    for no, item in enumerate(list_from_table):
        if list_from_table_answers[no] == "Ja":
            result_list.append(makeViable(item))
        else:
            result_list_noDemo.append(makeViable(item))
    duplicates = [item for item, count in collections.Counter(list_from_table).items() if count > 1]

    if not duplicates == []:  # is distinct
        class DuplicateError(Exception):
            pass

        raise DuplicateError(str(duplicates))

    random.shuffle(result_list)
    random.shuffle(result_list_noDemo)
    result_list = [*result_list, *result_list_noDemo]

    if len(result_list) % 2 == 1:
        if not messagebox.askokcancel("ODD NAME COUNT: ",
                str(len(result_list)) + " participants"):
            return None

    return result_list


def makeViable(string):
    # remove spaces
    string = string.replace(" ", "_")

    # remove illegal characters
    for char in "<>/*|\\§?:":
        string = string.replace(char, "#")

    # do not allow bad starts or endings
    if string.startswith(".") or string.startswith("_") or string.startswith("-"):
        string = "a" + string
    if string.endswith(".") or string.endswith("_") or string.endswith("-"):
        string += "a"

    return string


def generateFolder(alias_tupel):
    alias = alias_tupel[0]
    group = alias_tupel[1]

    dirpath = path_targetFolder + "/" + alias
    try:
        os.mkdir(dirpath)
    except FileExistsError:
        pass

    copyFiles(dirpath, group)


def copyFiles(dir, group):
    shutil.copy(path_slides, dir)
    if group == "A1" or group == "A2":
        shutil.copy(path_Werteliste_A, dir)
        if group == "A1":
            shutil.copy(path_InstructionA1, dir)
        else:
            shutil.copy(path_InstructionA2, dir)
    elif group == "B1" or group == "B2":
        shutil.copy(path_Werteliste_B, dir)
        if group == "B1":
            shutil.copy(path_InstructionB1, dir)
        else:
            shutil.copy(path_InstructionB2, dir)
    else:
        class GroupNotFoundException(Exception):
            pass

        raise GroupNotFoundException(group)


if __name__ == "__main__":
    generateGroups()
