import datetime
import xml.etree.ElementTree as ET
import os
import schedule
import time
from datetime import date
from library.getConnection import getConnection

# Названия контактов FIO, которые не добавляются в справочник
NO_NEED = ['Вакансия',
           'вакансия',
           'уборщицы',
           'Уборщицы',
           'Санитар',
           'Медицинский регистратор',
           'Вакант',
           'вакант',
           'Гараж',
           'Морг',
           'дежурный',
           ' вакансия ',
           'вакансия ',
           'ВАКАНТ',
           # 'Охрана',
           # 'Пост',

           ]

# Расшифровка num_obl для формирования групп абонентов по коду области
GROUP_BLR = {"1": "ЦА",
             "2": "Бресткая_обл",
             "3": "Витебская_обл",
             "4": "Гомельская_обл",
             "5": "Гродненская_обл",
             "6": "Минская_обл",
             "7": "Могилевская_обл",
             "8": "Минск",
             "9": "ИПКиПК",
             "11": "НПЦ",
             }

LIST_OF_COLUMNS = ["Name",
                   "Group",
                   "WorkPhone",
                   ]

# FILE_NAME_XML = os.path.abspath(rf"contact_{date.today().strftime("%Y_%m_%d")}.xml")
# FILE_NAME_XML_CA = os.path.abspath(rf"contact_CA_{date.today().strftime("%Y_%m_%d")}.xml")
# FILE_NAME_XML_SHOT = os.path.abspath(rf'contact_{date.today().strftime("%Y_%m_%d")}_name_shot.xml')
# FILE_NAME_XML_SHOT_CA = os.path.abspath(rf'contact_CA_{date.today().strftime("%Y_%m_%d")}_name_shot.xml')

LIST_OF_OUTPUT_FILES = [
    {
        "path": rf"\\10.10.12.198\uiis\PhoneBook\contact_ALL_{date.today().strftime("%Y_%m_%d")}.xml",
        "onlyCA": False,
        'longName': True,
    },
    {
        "path": rf"\\10.10.12.198\uiis\PhoneBook\contact_CA_{date.today().strftime("%Y_%m_%d")}.xml",
        "onlyCA": True,
        'longName': True,
    },
    {
        "path": rf'\\10.10.12.198\uiis\PhoneBook\contact_name_shot_ALL_{date.today().strftime("%Y_%m_%d")}.xml',
        "onlyCA": False,
        'longName': False,
    },
    {
        "path": rf'\\10.10.12.198\uiis\PhoneBook\contact_name_shot_CA_{date.today().strftime("%Y_%m_%d")}.xml',
        "onlyCA": True,
        'longName': False,
    },
]


def createXMLFile(fileName, *args, **kwargs):
    outputFile = open(fileName, 'w')
    outputFile.write("""<?xml version="1.0" encoding="UTF-8"?><PhoneBook></PhoneBook>""")
    outputFile.close()
    return outputFile


def convertPhonebookDataToList(d, *args, **kwargs):
    RESULT = []
    for element in d:
        t = {}
        for n, sense in enumerate(element):
            try:
                if n in [0]:
                    while '  ' in sense:
                        sense = sense.replace('  ', ' ')
                    if sense[0] == ' ':
                        sense = sense[1:]
                    if sense[-1] == ' ':
                        sense = sense[:-1]

                    if sense and (sense not in NO_NEED) and not ('декрет' in sense):
                        t.update({LIST_OF_COLUMNS[n]: sense})
                    else:
                        t.update({LIST_OF_COLUMNS[n]: None})

                elif n in [1]:
                    t.update({LIST_OF_COLUMNS[n]: sense}) if sense else t.update(
                        {LIST_OF_COLUMNS[n]: None})
                elif n in [2]:
                    while ' ' in sense:
                        sense = sense.replace(' ', '')
                    while '-' in sense:
                        sense = sense.replace('-', '')
                    t.update({LIST_OF_COLUMNS[n]: sense}) if sense else t.update({LIST_OF_COLUMNS[n]: None})

            except Exception as e:
                print(e)

        if t[LIST_OF_COLUMNS[0]]:
            RESULT.append(t)

    return RESULT


def formatDataForAdd(d, *args, **kwargs):
    for item in d:
        if item[LIST_OF_COLUMNS[0]] == 'Волков Алексей Александрович':
            item[LIST_OF_COLUMNS[2]] = '6300'

        if item[LIST_OF_COLUMNS[2]] == '6102':
            item[LIST_OF_COLUMNS[0]] = 'Оперативно-дежурная служба'

        if (item[LIST_OF_COLUMNS[1]] > 1 and item[LIST_OF_COLUMNS[1]] < 7) and len(item[LIST_OF_COLUMNS[2]]) < 5:
            item[LIST_OF_COLUMNS[2]] = f"7{item[LIST_OF_COLUMNS[1]] - 1}{item[LIST_OF_COLUMNS[2]]}"

        if item[LIST_OF_COLUMNS[1]] == 1 and len(item[LIST_OF_COLUMNS[2]]) > 8:
            item[LIST_OF_COLUMNS[2]] = item[LIST_OF_COLUMNS[2]][:4]

        if len(item[LIST_OF_COLUMNS[2]]) > 8 and '(' in item[LIST_OF_COLUMNS[2]]:
            item[LIST_OF_COLUMNS[2]] = item[LIST_OF_COLUMNS[2]].replace('(', '')
            item[LIST_OF_COLUMNS[2]] = item[LIST_OF_COLUMNS[2]].replace(')', '')
            item[LIST_OF_COLUMNS[2]] = f'9{item[LIST_OF_COLUMNS[2]]}'

        if item[LIST_OF_COLUMNS[1]] == 1 and len(item[LIST_OF_COLUMNS[2]]) == 7:
            item[LIST_OF_COLUMNS[2]] = f'9{item[LIST_OF_COLUMNS[2]]}'
    return d


def convertShotName(name, *args, **kwargs):
    s = name.split(' ')
    if (len(s) > 2) and ('пост' not in s[0]) and ('Пост' not in s[0]) and ('Охрана:' not in s[0]):
        n = s[1]
        sn = s[2]
        name = f'{s[0]} {n[0:1]}.{sn[0:1]}.'

    return name


def addContactToXML(d, root_f, only_ca=False, long_name=True, *args, **kwargs):
    print(f"Len(d): {len(d)}, only_ca: {only_ca}, long_name: {long_name} ")
    add_count = 0
    for item in d:
        if only_ca and item["Group"] != 1:
            continue

        add_count += 1
        new_elem = ET.Element('DirectoryEntry')
        root_f.append(new_elem)
        name = ET.SubElement(new_elem, 'Name')
        name.text = item.get("Name") if long_name else convertShotName(item.get("Name"))
        telephone = ET.SubElement(new_elem, 'Telephone')
        telephone.text = item.get("WorkPhone")
        mobile = ET.SubElement(new_elem, 'Mobile')
        other = ET.SubElement(new_elem, 'Other')
        ring = ET.SubElement(new_elem, 'Ring')
        ring.text = 'Default'
        group = ET.SubElement(new_elem, 'Group')
        group.text = GROUP_BLR.get(str(item.get("Group")))

    print(f"add_count: {add_count}")
    return root_f


def mainConverter(data=[], *args, **kwargs):
    try:
        try:
            cursor, connection = getConnection()
            cursor.execute(
                f'SELECT FIO, num_obl, WorkPhone FROM BookNumbers WHERE WorkPhone IS NOT NULL AND FIO IS NOT NULL')
            data = cursor.fetchall()
        except Exception as e:
            print('001 Ошибка соединения и получения данных из базы: ', e)
        finally:
            cursor.close()
            connection.close()

        try:
            data = convertPhonebookDataToList(data)
        except Exception as e:
            print('002 Ошибка конвертации базы: ', e)

        try:
            data = formatDataForAdd(data)
        except Exception as e:
            print('003 Ошибка форматирования даннных: ', e)

        for file in LIST_OF_OUTPUT_FILES:
            try:
                createXMLFile(file["path"])
                tree = ET.parse(file["path"])
                root = addContactToXML(data, tree.getroot(), only_ca=file["onlyCA"], long_name=file["longName"])
                tree.write(file["path"])
            except Exception as e:
                print(
                    f'004 Ошибка создания и добавления данных в файл справочника file: {file["path"]} only_ca: {file["onlyCA"]} long_name={file["longName"]}:: ',
                    e)

    except Exception as e:
        print('Ошибка обработки полученных данных и формирования справочника: ', e)
    else:
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), 'Make phoneBook is OK!')


mainConverter()

# schedule.every(1).minutes.do(mainConverter)
# schedule.every().day.at("14:00:00").do(mainConverter)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
#
#
