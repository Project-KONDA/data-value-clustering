import numpy
import pandas

from workshop.copy_analysis_forms import path_excel_clustering, path_excel_werteliste
from workshop.generate_folders import alias_pairs_file_name, SEPARATOR, makeViable


def check_missing_partners():
    _check_missing_partners(path_excel_clustering, "clustering")
    _check_missing_partners(path_excel_werteliste, "werteliste")


def _check_missing_partners(path_excel, type_string):
    with open(alias_pairs_file_name) as f:
        for line in f:
            line = line.replace("\n", "")
            split = line.split(SEPARATOR)
            assert len(split) <= 2
            alias = split[0]
            if len(split) > 1:
                partner = split[1]
                table = numpy.array(pandas.read_excel(path_excel, sheet_name=0, header=0))
                found = False
                for n in table[:, 1]:
                    if isinstance(n, str) and makeViable(n) == partner:
                        found = True
                if not found:
                    print("'" + alias + "' has a partner ('" + partner + "') who did not submit the " + type_string + " questionnaire")
            else:
                print("'" + alias + "' does not have a partner")



if __name__ == "__main__":
    check_missing_partners()