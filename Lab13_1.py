class Note:
    def __init__(self, last_name, first_name, phone_number, birth_date):
        self.last_name = last_name
        self.first_name = first_name
        self.phone_number = phone_number
        self.birth_date = birth_date

class TrieNode:
    def __init__(self):
        self.children = {}
        self.note = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, note):
        node = self.root
        for char in note.phone_number:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.note = note

    def search(self, phone_number):
        node = self.root
        for char in phone_number:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.note

    def delete(self, phone_number):
        def _delete(node, idx):
            if idx == len(phone_number):
                if node.note is not None:
                    node.note = None
                    return len(node.children) == 0
                return False

            char = phone_number[idx]
            if char not in node.children:
                return False

            if _delete(node.children[char], idx + 1):
                del node.children[char]
                return len(node.children) == 0 and node.note is None

            return False

        _delete(self.root, 0)

    def delete_by_name(self, first_name, last_name):
        def _delete_by_name(node, notes_to_delete):
            if node.note is not None and node.note.first_name == first_name and node.note.last_name == last_name:
                notes_to_delete.append(node.note.phone_number)
            for child in node.children.values():
                _delete_by_name(child, notes_to_delete)

        notes_to_delete = []
        _delete_by_name(self.root, notes_to_delete)
        for phone_number in notes_to_delete:
            self.delete(phone_number)

    def delete_by_birth_date(self, birth_date):
        def _delete_by_birth_date(node, notes_to_delete):
            if node.note is not None and node.note.birth_date == birth_date:
                notes_to_delete.append(node.note.phone_number)
            for child in node.children.values():
                _delete_by_birth_date(child, notes_to_delete)

        notes_to_delete = []
        _delete_by_birth_date(self.root, notes_to_delete)
        for phone_number in notes_to_delete:
            self.delete(phone_number)

def save_to_file(trie, file_name):
    def serialize(node, prefix):
        serialized_node = []
        if node.note is not None:
            serialized_node.append(f"{prefix} {node.note.last_name} {node.note.first_name} {' '.join(map(str, node.note.birth_date))}")
        for char, child in node.children.items():
            serialized_node.extend(serialize(child, prefix + char))
        return serialized_node

    with open(file_name, "w") as file:
        file.writelines([line + "\n" for line in serialize(trie.root, "")])

def load_from_file(file_name):
    trie = Trie()

    with open(file_name, "r") as file:
        for line in file.readlines():
            parts = line.strip().split(" ")
            phone_number = parts[0]
            last_name = parts[1]
            first_name = parts[2]
            birth_date = list(map(int, parts[3:]))
            note = Note(last_name, first_name, phone_number, birth_date)
            trie.insert(note)

    return trie

def display_trie(trie):
    def traverse(node, prefix):
        if node.note is not None:
            print(f"Прізвище: {node.note.last_name}")
            print(f"Ім'я: {node.note.first_name}")
            print(f"Номер телефону: {node.note.phone_number}")
            print(f"Дата народження: {'.'.join(map(str, node.note.birth_date))}")
            print()

        for char, child in node.children.items():
            traverse(child, prefix + char)

    traverse(trie.root, "")

def is_leap_year(year):
    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True

def days_in_month(month, year):
    if month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 29 if is_leap_year(year) else 28
    else:
        return 31

def is_valid_date(day, month, year):
    if year < 1 or month < 1 or month > 12 or day < 1:
        return False
    return day <= days_in_month(month, year)

trie = Trie()
while True:
        print("1: Додати контакт")
        print("2: Знайти контакт")
        print("3: Видалити контакт")
        print("4: Зберегти дані у файл")
        print("5: Завантажити дані з файлу")
        print("6: Вивести всі контакти")
        print("0: Вийти")

        try:
            choice = input("Введіть номер опції: ")

        except (EOFError, KeyboardInterrupt):
            print("Неправильний формат")
            break

        if choice == "1":
            last_name = input("Введіть прізвище: ")
            first_name = input("Введіть ім'я: ")
            phone_number = input("Введіть номер телефону: ")

            while True:
                birth_date = list(map(int, input("Введіть дату народження (день місяць рік): ").split()))
                if len(birth_date) == 3 and is_valid_date(*birth_date):
                    break
                else:
                    print("Некоректна дата народження. Спробуйте ще раз.")

            note = Note(last_name, first_name, phone_number, birth_date)
            trie.insert(note)
            print("Контакт додано.")

        elif choice == "2":
            while True:
                print("1: Знайти контакт за номером телефону")
                print("2: Знайти контакт за іменем та прізвищем")
                print("3: Знайти контакт за датою народження")
                print("4: Назад")

                search_choice = input("Введіть номер опції для пошуку: ")

                if search_choice == "1":
                    phone_number = input("Введіть номер телефону: ")
                    note = trie.search(phone_number)
                    if note is None:
                        print("Контакт не знайдено.")
                    else:
                        print(f"Прізвище: {note.last_name}")
                        print(f"Ім'я: {note.first_name}")
                        print(f"Номер телефону: {note.phone_number}")
                        print(f"Дата народження: {'.'.join(map(str, note.birth_date))}")

                elif search_choice == "2":
                    last_name = input("Введіть прізвище: ")
                    first_name = input("Введіть ім'я: ")
                    found_notes = trie.search_by_name(first_name, last_name)
                    if not found_notes:
                        print("Контакти не знайдено.")
                    else:
                        for note in found_notes:
                            print(f"Прізвище: {note.last_name}")
                            print(f"Ім'я: {note.first_name}")
                            print(f"Номер телефону: {note.phone_number}")
                            print(f"Дата народження: {'.'.join(map(str, note.birth_date))}")
                            print()

                elif search_choice == "3":
                    birth_date = list(map(int, input("Введіть дату народження (день місяць рік): ").split()))
                    found_notes = trie.search_by_birth_date(birth_date)
                    if not found_notes:
                        print("Контакти не знайдено.")
                    else:
                        for note in found_notes:
                            print(f"Прізвище: {note.last_name}")
                            print(f"Ім'я: {note.first_name}")
                            print(f"Номер телефону: {note.phone_number}")
                            print(f"Дата народження{'.'.join(map(str, note.birth_date))}")
                            print()
                elif search_choice == "4":
                    break
        elif choice == "3":
            while True:
                print("1: Видалити контакт за номером телефону")
                print("2: Видалити контакт за іменем та прізвищем")
                print("3: Видалити контакт за датою народження")
                print("4: Назад")

                delete_choice = input("Введіть номер опції для видалення: ")

                if delete_choice == "1":
                    phone_number = input("Введіть номер телефону: ")
                    trie.delete(phone_number)
                    print("Контакт видалено.")

                elif delete_choice == "2":
                    last_name = input("Введіть прізвище: ")
                    first_name = input("Введіть ім'я: ")
                    trie.delete_by_name(first_name, last_name)
                    print("Контакт(и) видалено(і).")

                elif delete_choice == "3":
                    birth_date = list(map(int, input("Введіть дату народження (день місяць рік): ").split()))
                    trie.delete_by_birth_date(birth_date)
                    print("Контакт(и) видалено(і).")

                elif delete_choice == "4":
                    break

                else:
                    print("Невідома опція. Спробуйте ще раз.")

        elif choice == "4":
            file_name = input("Введіть ім'я файлу: ")
            save_to_file(trie, file_name)
            print("Дані збережено у файл.")

        elif choice == "5":
            file_name = input("Введіть ім'я файлу: ")
            try:
                trie = load_from_file(file_name)
                print("Дані завантажено з файлу.")
            except FileNotFoundError:
                print("Файл не знайдено.")

        elif choice == "6":
            print("Усі контакти:")
            display_trie(trie)

        elif choice == "0":
            print("До побачення!")
            break

        else:
            print("Невідома опція. Спробуйте ще раз.")