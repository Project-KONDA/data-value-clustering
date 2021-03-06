import glob
import os
import shutil

import numpy
import pandas as pd

from workshop.generate_folders import alias_pairs_file_name, makeViable, SEPARATOR

path_target_folder = "../../mock_dir/"  # replace with .../PublicWorkshopFolders/KONDAClusteringWorkshop/

path_source_folder_clustering = "./workshop_files/analysis_forms/clustering/"
path_source_folder_werteliste = "./workshop_files/analysis_forms/werteliste/"
path_excel_clustering = "./workshop_files/analysis_forms/Fragebogen zum Clustering.xlsx"
path_excel_werteliste = "./workshop_files/analysis_forms/Fragebogen zur Werteliste.xlsx"
file_name_prefix_clustering = "Fragebogen zum Clustering - "
file_name_prefix_werteliste = "Fragebogen zur Werteliste - "


def copy_analysis_forms():
    _copy_analysis_forms(path_excel_clustering, path_source_folder_clustering, file_name_prefix_clustering)
    _copy_analysis_forms(path_excel_werteliste, path_source_folder_werteliste, file_name_prefix_werteliste)


def _copy_analysis_forms(path_excel, path_source_folder, file_name_prefix):
    table = numpy.array(pd.read_excel(path_excel, sheet_name=0, header=0))
    os.chdir(path_source_folder)
    for file in glob.glob("*.pdf"):
        id = int(file.replace(file_name_prefix, "").replace(".pdf", ""))
        line = numpy.where(table[:, 0] == id)[0][0]
        this_alias = makeViable(table[line, 1])
        other_alias = None
        alias_found = False
        with open("../../../" + alias_pairs_file_name) as f:
            for line in f:
                line = line.replace("\n","")
                split = line.split(SEPARATOR)
                assert len(split) <= 2
                if split[0] == this_alias:
                    alias_found = True
                    if len(split) == 2:
                        other_alias = split[1]
                    else:
                        other_alias = None
                        continue

        if not alias_found:
            print("ALIAS NOT FOUND ERROR: '" + this_alias + "'. File '" + file + "' was not copied at all.")
            continue

        file_name = file_name_prefix + this_alias + ".pdf"

        this_target_file = path_target_folder + this_alias + "/" + file_name
        try:
            shutil.copy(file, this_target_file)
        except FileNotFoundError as e:
            print("INVALID ALIAS ERROR: file '" + file + "' should have been copied to author directory '" + this_target_file + "' but a FileNotFoundError was raised")

        if other_alias is None:
            print("NO PARTNER ERROR: '" + this_alias + "'. File '" + file + "' was not copied to partner directory and " + this_alias + " did not receive partner questionnaires.")
            continue

        other_target_file = path_target_folder + other_alias + "/" + file_name
        try:
            shutil.copy(file, other_target_file)
        except FileNotFoundError as e:
            print("INVALID ALIAS ERROR: file '" + file + "' should have been copied to partner directory '" + other_target_file + "' but a FileNotFoundError was raised")

    os.chdir("../../../")


if __name__ == "__main__":
    copy_analysis_forms()