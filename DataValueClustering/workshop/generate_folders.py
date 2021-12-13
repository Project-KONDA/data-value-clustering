import os
import re
import shutil

path_targetFolder = "./workshop_clustering_tool"

path_slides = "./workshop_files/Folien.pdf"
path_alias_Table = "./workshop_files/alias.xlsx"

# path_InstructionA1 = "./workshop_files/Anleitung_GruppeA1.pdf"
# path_InstructionB1 = "./workshop_files/Anleitung_GruppeB1.pdf"
# path_InstructionA2 = "./workshop_files/Anleitung_GruppeA2.pdf"
# path_InstructionB2 = "./workshop_files/Anleitung_GruppeB2.pdf"

path_InstructionA1 = "./workshop_files/Anleitung_Gruppe_A1_Pilot.pdf"
path_InstructionB1 = "./workshop_files/Anleitung_Gruppe_B1_Pilot.pdf"
path_InstructionA2 = "./workshop_files/Anleitung_Gruppe_A2_Pilot.pdf"
path_InstructionB2 = "./workshop_files/Anleitung_Gruppe_B2_Pilot.pdf"

path_Werteliste_A = "./workshop_files/RepositoryName_Werteliste.xlsx"
path_Werteliste_B = "./workshop_files/ActorName_Werteliste.xlsx"
# path_Werteliste_C = "./workshop_files/RepositoryLocationName_Werteliste.xlsx"


def generateGroups():
    alias_list = readAliasList(path_alias_Table)
    if alias_list is None:
        return

    groups = ("A1", "B2", "A2", "B1")
    division = list()

    for i, alias in enumerate(alias_list):
        t = (alias, groups[i % 4], i // 2)
        division.append(t)

    textfile = open("alias.txt", "w")
    for i, element in enumerate(division):
        textfile.write(element[0] + "|" + element[1] + "|" + str(element[2]) + "\n")
    textfile.close()
    textfile2 = open("alias_pairs.txt", "w")
    for i in range(len(division)//2):
        assert (division[i * 2][2] == division[i * 2 + 1][2])
        textfile2.write(division[i * 2][0] + "|" + division[i * 2 + 1][0] + "\n")
        textfile2.write(division[i * 2 + 1][0] + "|" + division[i * 2][0] + "\n")
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

    result_list = []
    for item in list_from_table:
        result_list.append(makeViable(item))

    duplicates = [item for item, count in collections.Counter(list_from_table).items() if count > 1]

    if not duplicates == []:  # is distinct
        class DuplicateError(Exception):
            pass

        raise DuplicateError(str(duplicates))

    if len(result_list) % 2 == 1:
        if not messagebox.askokcancel("ODD NAME COUNT: ",
                str(len(result_list)) + " participants"):
            return None


    random.shuffle(result_list)
    return result_list


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
