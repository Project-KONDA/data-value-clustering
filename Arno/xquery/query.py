from BaseXClient import BaseXClient


def execute_xquery(my_query, database=""):
    input = my_query

    if database != "":
        input = 'doc("' + database + '")' + my_query

    print("Executing: " + input)
    # create session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        query = session.query(input)

        result = list()
        for typecode, item in query.iter():
            result.append(item)

        query.close()
        return result
    finally:
        if session:
            session.close()


if __name__ == "__main__":
    li = execute_xquery("//concept/data()", "APS_FME-private-OBJ")
    print(li)
