import csv
import re

# TODO 1: выполните пункты 1-3 ДЗ
pattern = r'^(\+7|8)?\D*(\d{3})\D*(\d{3})\D*(\d{2})\D*(\d{2})(?:\D*(\d{1,10}))?\D*$'

def normolized_phone(match):
    base = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
    if match.group(6):  # Если есть добавочный номер
        return f"{base} доб.{match.group(6)}"
    else:
        return base

contacts_list = []

# Читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    reader_dict = csv.DictReader(f)
    for row in reader_dict:
        contacts_list.append(row)

merged_contacts = {}

for contact in contacts_list:
    fio_parts = []
    for field in ['lastname', 'firstname', 'surname']:
        if contact[field]:
            fio_parts.extend(contact[field].strip().split())

    if len(fio_parts) == 3:
        lastname, firstname, surname = fio_parts[0], fio_parts[1], fio_parts[2]

    final_key = (lastname, firstname, surname)

    if final_key not in merged_contacts:
        merged_contacts[final_key] = {
            'organization': '',
            'position': '',
            'phone': '',
            'email': ''
        }

    current_data = merged_contacts[final_key]

    # Обрабатываем значения в merged_contacts по ключу
    if contact['organization'] and not current_data['organization']:
        current_data['organization'] = contact['organization'].strip()

    if contact['position'] and not current_data['position']:
        current_data['position'] = contact['position'].strip()

    if contact['phone'] and not current_data['phone']:
        current_data['phone'] = re.sub(pattern, normolized_phone, contact['phone'])

    if contact['email'] and not current_data['email']:
        current_data['email'] = contact['email'].strip()

# Преобразуем обратно в список словарей для CSV
result_contacts = []
for (lastname, firstname, surname), data in merged_contacts.items():
    contact = {
        'lastname': lastname,
        'firstname': firstname,
        'surname': surname,
        'organization': data['organization'],
        'position': data['position'],
        'phone': data['phone'],
        'email': data['email']
    }
    result_contacts.append(contact)

# Сортируем данные по Фамилии
result_contacts_sorted = sorted(result_contacts, key=lambda x: x['lastname'])

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    fieldnames = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(result_contacts_sorted)