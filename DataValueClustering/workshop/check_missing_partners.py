import numpy
import pandas

from workshop.copy_analysis_forms import path_excel_clustering, path_excel_werteliste
from workshop.generate_folders import alias_pairs_file_name, SEPARATOR, makeViable, alias_file_name


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
                    with open(alias_file_name) as f2:
                        for line2 in f2:
                            line2 = line2.replace("\n", "")
                            split2 = line2.split(SEPARATOR)
                            if split2[0] == alias:
                                self_group = split2[1]
                            if split2[0] == partner:
                                partner_group = split2[1]

                    print("'" + alias + "' (group " + self_group + ") has a partner ('" + partner + "', group " + partner_group + ") who did not submit the " + type_string + " questionnaire")
            else:
                print("'" + alias + "' (group " + self_group + ") did not have a partner from the beginning")



if __name__ == "__main__":
    check_missing_partners()