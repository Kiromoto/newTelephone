from library.getConnection import getConnection

REGIONS = [1, 2, 3, 4, 5, 6, 7, 8, ]

GROUP_BLR = {
    1: "ЦА",
    2: "Бресткая_обл",
    3: "Витебская_обл",
    4: "Гомельская_обл",
    5: "Гродненская_обл",
    6: "Минская_обл",
    7: "Могилевская_обл",
    8: "Минск"
}


def mainGetStat(data=[], *args, **kwargs):
    cursor, connection = getConnection()
    if cursor:
        for region in REGIONS:
            all_rows, photo_count, phone_count, mobile_count = 0, 0, 0, 0
            try:
                cursor.execute(f'SELECT * FROM BookNumbers WHERE num_obl=%d', region)
                data = cursor.fetchall()
                # row[0] = ID
                # row[1] = FIO
                # row[2] = DepartmentsID
                # row[3] = Positions
                # row[4] = Photo
                # row[5] = Address
                # row[6] = WorkPhone
                # row[7] = MobilePhone
                # row[8] = CityPhone
                # row[9] = MobilePhone2
                # row[10] = CityPhone2
                # row[11] = CenrixPhone
                # row[12] = SMPhone
                # row[13] = num_obl
                # row[14] = ReceptionPhone
                # row[14] = Fax

                for row in data:
                    if not row[3]:
                        continue

                    if row[1]:
                        all_rows += 1
                    if row[4]:
                        photo_count += 1
                    if row[6] or row[8] or row[10]:
                        phone_count += 1
                    if row[7] or row[9]:
                        mobile_count += 1

            except Exception as e:
                print(f'Ошибка получения даннных из базы region={region} : {e}')
            else:
                print(
                    f'{GROUP_BLR.get(region)}. Всего записей={all_rows} Фото={photo_count} ({photo_count / all_rows * 100:.2f}%) Рабочий={phone_count} ({phone_count / all_rows * 100:.2f}%) Мобильный={mobile_count} ({mobile_count / all_rows * 100:.2f}%)')
        cursor.close()
        connection.close()


mainGetStat()
