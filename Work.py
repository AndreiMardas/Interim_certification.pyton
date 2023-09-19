import json
import datetime

# Функция для создания новой заметки
def create_note():
    note_id = input("Введите идентификатор заметки: ")
    title = input("Введите заголовок заметки: ")
    body = input("Введите содержание заметки: ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"id": note_id, "title": title, "body": body, "timestamp": timestamp}

# Функция для сохранения заметки в файл
def save_note(note, filename):
    with open(filename, 'a') as file:
        file.write(json.dumps(note) + '\n')

# Функция для чтения списка заметок из файла
def read_notes(filename):
    notes = []
    with open(filename, 'r') as file:
        for line in file:
            note = json.loads(line)
            notes.append(note)
    return notes

# Функция для вывода списка заметок с возможностью фильтрации по дате
def show_notes(notes, filter_date=None):
    for note in notes:
        note_date = datetime.datetime.strptime(note['timestamp'], "%Y-%m-%d %H:%M:%S")
        if filter_date is None or note_date.date() == filter_date:
            print("Идентификатор:", note['id'])
            print("Заголовок:", note['title'])
            print("Содержание:", note['body'])
            print("Дата/время создания:", note['timestamp'])
            print()

# Функция для редактирования заметки
def edit_note(note):
    new_title = input("Введите новый заголовок (оставьте пустым, чтобы оставить без изменений): ")
    new_body = input("Введите новое содержание (оставьте пустым, чтобы оставить без изменений): ")
    if new_title:
        note['title'] = new_title
    if new_body:
        note['body'] = new_body
    note['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Функция для удаления заметки
def delete_note(note_id, filename):
    notes = read_notes(filename)
    notes = [note for note in notes if note['id'] != note_id]
    with open(filename, 'w') as file:
        for note in notes:
            file.write(json.dumps(note) + '\n')

# Основная функция приложения
def main():
    filename = "notes.json"  # имя файла для сохранения заметок

    while True:
        print("Выберите действие:")
        print("1. Создать новую заметку")
        print("2. Показать список заметок")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Выйти из программы")
        choice = input("Введите номер действия: ")

        if choice == "1":
            note = create_note()
            save_note(note, filename)
            print("Заметка успешно создана и сохранена.\n")

        elif choice == "2":
            notes = read_notes(filename)
            date_filter = input("Введите дату для фильтрации (гггг-мм-дд) или оставьте пустым для показа всех заметок: ")
            if date_filter:
                try:
                    filter_date = datetime.datetime.strptime(date_filter, "%Y-%m-%d").date()
                    show_notes(notes, filter_date)
                except ValueError:
                    print("Некорректный формат даты.")
            else:
                show_notes(notes)

        elif choice == "3":
            note_id = input("Введите идентификатор заметки для редактирования: ")
            notes = read_notes(filename)
            for note in notes:
                if note['id'] == note_id:
                    edit_note(note)
                    break
            with open(filename, 'w') as file:
                for note in notes:
                    file.write(json.dumps(note) + '\n')
            print("Заметка успешно отредактирована.\n")

        elif choice == "4":
            note_id = input("Введите идентификатор заметки для удаления: ")
            delete_note(note_id, filename)
            print("Заметка успешно удалена.\n")

        elif choice == "5":
            break

        else:
            print("Некорректный выбор.")

if __name__ == "__main__":
    main()