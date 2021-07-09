from datetime import datetime
from BaseXClient import BaseXClient

from data_extraction.write_file import write_data_values_to_file


def write_fielddata_from_xml(xmlfile, field):

    query = "//*[name()=\"" + field + "\"]/text()"
    values = execute_xquery(query, xmlfile)
    print(values)

    if len(values) > 0:
        dbname = xmlfile.split('\\')
        dbname = dbname[len(dbname)-1].split('.')
        dbname = dbname[0]
        filename = field + "_" + dbname + "_" + datetime.now().strftime("%Y%m%d-%H%M%S")+ ".txt"
        filename = "../data/" + filename
        write_data_values_to_file(filename, values)


def execute_xquery(my_query, database):
    input = 'doc("' + database + '")' + my_query
    result = []

    print("Executing: " + input)
    # create session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        query = session.query(input)

        result = list()
        for typecode, item in query.iter():
            result.append(item)

        query.close()
    except Exception:
        print("Fail")
    finally:
        if session:
            session.close()
        return result


if __name__ == '__main__':
    file = 'F:\KONDA_GoogleDrive\KONDA AV\Daten\APS_Midas\\fme-private-seiten20200224.aps.xml.gz'
    field = 'a2864'
    write_fielddata_from_xml(file, field)
