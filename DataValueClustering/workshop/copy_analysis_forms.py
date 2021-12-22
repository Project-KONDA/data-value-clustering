import glob
import os
import shutil

import numpy
import pandas as pd

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
        this_alias = table[line, 1]
        other_alias = table[line, 2]
        file_name = file_name_prefix + this_alias + ".pdf"

        this_target_file = path_target_folder + this_alias + "/" + file_name
        other_target_file = path_target_folder + other_alias + "/" + file_name
        shutil.copy(file, this_target_file)
        shutil.copy(file, other_target_file)
    os.chdir("../../../")


if __name__ == "__main__":
    copy_analysis_forms()