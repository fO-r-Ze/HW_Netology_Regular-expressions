import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

pattern = r'^(\+7|8)?\D*(\d{3})\D*(\d{3})\D*(\d{2})\D*(\d{2})(?:\D*(\d{1,10}))?\D*$'

def replacement(match):
    base = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
    if match.group(6):  # Если есть добавочный номер
        return f"{base} доб.{match.group(6)}"
    else:
        return base

# TODO 1: выполните пункты 1-3 ДЗ
new_list = []
for contact in contacts_list:
    name = ' '.join(contact[0:3])
    organization = contact[3]
    position = contact[4]
    phone = re.sub(pattern, replacement, contact[5])
    email = contact[6]
    try:
        last_name = name.split()[0]
        first_name = name.split()[1]
        surname = name.split()[2]
    except IndexError:
        surname = ""
    new_list.append([last_name, first_name, surname, organization, position, phone, email])

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(new_list)