from library.getConnection import getConnection
import re

CITY_PHONE_CODE = {"1": ["017", ],
                   "2": ["01655", "01652", "01651", "01647", "01646", "01645", "01644", "01643",
                         "01642", "01641", "01633", "01632", "01631", "0165", "0163", "0162", ],
                   "3": ["02159", "02158", "02157", "02156", "02155", "02154", "02153", "02152", "02151", "02139",
                         "02138", "02137", "02136", "02135", "02133", "02132", "02131", "02130", "0216", "0214",
                         "0212", ],
                   "4": ["02357", "02356", "02355", "02354", "02353", "02350", "02347", "02346", "02345", "02344",
                         "02342", "02340", "02339", "02337", "02336", "02334", "02333", "02332", "02330", "0236",
                         "0232", ],
                   "5": ["01597", "01596", "01595", "01594", "01593", "01592", "01591", "01564", "01563", "01562",
                         "01515", "01514", "01513", "01512", "01511", "0154", "0152", ],
                   "6": ["01797", "01796", "01795", "01794", "01793", "01792", "01776", "01775", "01774", "01772",
                         "01771", "01770", "01767", "01719", "01718", "01717", "01716", "01715", "01714", "01713",
                         "0177", "0176", "0174", "017", ],
                   "7": ["02248", "02247", "02246", "02245", "02244", "02243", "02242", "02241", "02240", "02239",
                         "02238", "02237", "02236", "02235", "02234", "02233", "02232", "02231", "02230", "0225",
                         "0222", ],
                   "8": ["017", ],
                   "9": ["017", ],
                   "11": ["017", ],
                   }


def formatWorkNumbers(workNumerList=[], *args, **kwargs):
    for n, one_numer in enumerate(workNumerList):
        if one_numer[1]:
            only_digits = re.sub(r"[^0-9]", "", one_numer[1])
            if len(only_digits) >= 4:
                workNumerList[n][1] = f"{only_digits[:2]}-{only_digits[2:]}"

    return workNumerList


def formatMobilePhones(workNumerList=[], *args, **kwargs):
    for n, one_numer in enumerate(workNumerList):
        if one_numer[1]:
            only_digits = re.sub(r"[^0-9]", "", one_numer[1].replace("(А1)", ""))
            if len(only_digits) >= 9:
                workNumerList[n][
                    1] = f"+375({only_digits[-9:-7]}) {only_digits[-7:-4]}-{only_digits[-4:-2]}-{only_digits[-2:]}"

    return workNumerList


def formatCityNumbers(workNumerList=[], *args, **kwargs):
    for n, one_numer in enumerate(workNumerList):
        if one_numer[1]:
            only_digits = re.sub(r"[^0-9]", "", one_numer[1])
            if one_numer[2] in [1, 8, 9, 11]:
                if len(only_digits) == 7:
                    workNumerList[n][1] = f"8(017) {only_digits[:3]}-{only_digits[3:5]}-{only_digits[5:7]}"
                elif len(only_digits) > 7:
                    workNumerList[n][1] = f"8(017) {only_digits[-7:-4]}-{only_digits[-4:-2]}-{only_digits[-2:]}"
            else:
                codes = CITY_PHONE_CODE.get(str(one_numer[2]), [])
                workNumerList[n][1] = only_digits
                for code in codes:
                    if code in only_digits:
                        if only_digits.index(code) >= 0 and only_digits.index(code) <= 2:
                            index = only_digits.index(code) + len(code)
                            if len(only_digits[index:]) == 7 and code == '017':
                                workNumerList[n][1] = f"8({code}) {only_digits[index:index + 3]}-{only_digits[index + 3:index + 5]}-{only_digits[index + 5:]}"
                            elif len(only_digits[index:]) == 6:
                                workNumerList[n][1] = f"8({code}) {only_digits[index:index+2]}-{only_digits[index+2:index+4]}-{only_digits[index+4:]}"
                            elif len(only_digits[index:]) == 5:
                                workNumerList[n][1] = f"8({code}) {only_digits[index:index+1]}-{only_digits[index+1:index+3]}-{only_digits[index+3:]}"
                            else:
                                workNumerList[n][1] = f"8({code}) {only_digits[index:]}"
                            break

    return workNumerList


COLUMNS = [
    # {
    #     "name": "WorkPhone",
    #     "format_func": formatWorkNumbers,
    # },
    {
        "name": "СityPhone",
        "format_func": formatCityNumbers,
    },
    # {
    #     "name": "CentrixPhone",
    #     "format_func": formatWorkNumbers,
    # },
    # {
    #     "name": "MobilePhone",
    #     "format_func": formatMobilePhones,
    # },
    # {
    #     "name": "MobilePhone2",
    #     "format_func": formatMobilePhones,
    # },

]


def getWorkNumbers(*args, **kwargs):
    data = []
    try:
        cursor, connection = getConnection()
        cursor.execute(
            f'SELECT ID, WorkPhone FROM BookNumbers')
        data = cursor.fetchall()
    except Exception as e:
        print('Ошибка соединения и получения WorkPhone из BookNumbers: ', e)
    else:
        for numer, element in enumerate(data):
            data[numer] = list(element)

        return formatWorkNumbers(data)
    finally:
        cursor.close()
        connection.close()


def updateData(data=[], name_column=None, *args, **kwargs):
    cursor, connection = getConnection()
    update_query = f"""UPDATE BookNumbers SET {name_column} = %s WHERE ID = %s"""

    update_all, update_ok, update_error = 0, 0, 0
    for element in data:
        if element[1] is None:
            continue

        update_all += 1
        try:
            values = (str(element[1]), int(element[0]))
            cursor.execute(update_query, values)
        except Exception as e:
            update_error += 1
            connection.rollback()
            print(f'Ошибка обновления {name_column}. {element} в BookNumbers: {e}')
        else:
            connection.commit()
            update_ok += 1

    cursor.close()
    connection.close()
    print(
        f'Обновление столбца {name_column} завершено. Всего обновлено записей: {update_all}, из них успешно - {update_ok}, с ошибкой - {update_error}.')


def getData(name_column=None, format_func=None, *args, **kwargs):
    d = []
    try:
        cursor, connection = getConnection()
        if name_column == "СityPhone":
            cursor.execute(f"""SELECT ID, {name_column}, num_obl FROM BookNumbers""")
        else:
            cursor.execute(f"""SELECT ID, {name_column} FROM BookNumbers""")
        d = cursor.fetchall()
    except Exception as e:
        print(f"Ошибка соединения и получения {name_column} из BookNumbers: ", e)
    else:
        for numer, element in enumerate(d):
            d[numer] = list(element)

        return format_func(d)
    finally:
        cursor.close()
        connection.close()


for one_column in COLUMNS:
    data = getData(name_column=one_column["name"], format_func=one_column["format_func"])
    updateData(data=data, name_column=one_column["name"])
    # for element in data:
    #     if element[1] and element[2] == 5:
    #         print(element)
