import pickle
import re
from datetime import date, timedelta

file_name = 'address_book.pkl'

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


class AddressBook:
    def __init__(self):
        self.contacts = {}

    def save_to_file(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.contacts, file)

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                self.contacts = pickle.load(file)
        except FileNotFoundError:
            self.contacts = {}

    def is_valid_phone(self, phone):
        return re.match(r"^\d{10}$", phone)

    def add_contact(self, name, phone):
        if self.is_valid_phone(phone):
            self.contacts[name] = phone
            print("Contact added.")
        else:
            print("Invalid phone number format. Phone number must be 10 digits.")

    def change_contact(self, name, new_phone):
        if name in self.contacts:
            if self.is_valid_phone(new_phone):
                self.contacts[name] = new_phone
                print("Contact updated.")
            else:
                print("Invalid phone number format. Phone number must be 10 digits.")
        else:
            print("Contact not found.")

    def show_phone(self, name):
        if name in self.contacts:
            print(self.contacts[name])
        else:
            print("Contact not found.")

    def show_all(self):
        if self.contacts:
            for name, phone in self.contacts.items():
                print(f"{name}: {phone}")
        else:
            print("No contacts saved.")

    def add_birthday(self, name, birthday):
        self.contacts[name] = (self.contacts.get(name, ""), birthday)

    def show_birthday(self, name):
        contact_info = self.contacts.get(name)
        if contact_info:
            phone, birthday = contact_info
            print(f"{name}'s birthday: {birthday}")
        else:
            print("Contact not found.")

    def get_birthdays_per_week(self):
        today = date.today()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for name, contact_info in self.contacts.items():
            _, birthday = contact_info
            if birthday:
                day, month, _ = map(int, birthday.split('.'))
                if today <= date(today.year, month, day) <= next_week:
                    upcoming_birthdays.append((name, birthday))
        return upcoming_birthdays


def main():
    print("Welcome to the assistant bot!")
    book = AddressBook()
    book.load_from_file(file_name)

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            book.save_to_file(file_name)
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            if len(args) == 2:
                name, phone = args
                book.add_contact(name, phone)
            else:
                print("Invalid command. Usage: add [name] [phone]")
        elif command == "change":
            if len(args) == 2:
                name, new_phone = args
                book.change_contact(name, new_phone)
            else:
                print("Invalid command. Usage: change [name] [new_phone]")
        elif command == "phone":
            if len(args) == 1:
                name = args[0]
                book.show_phone(name)
            else:
                print("Invalid command. Usage: phone [name]")
        elif command == "all":
            book.show_all()
        elif command == "add-birthday":
            if len(args) == 2:
                name, birthday = args
                book.add_birthday(name, birthday)
            else:
                print("Invalid command. Usage: add-birthday [name] [birthday]")
        elif command == "show-birthday":
            if len(args) == 1:
                name = args[0]
                book.show_birthday(name)
            else:
                print("Invalid command. Usage: show-birthday [name]")
        elif command == "birthdays":
            upcoming_birthdays = book.get_birthdays_per_week()
            if upcoming_birthdays:
                print("Upcoming birthdays:")
                for name, birthday in upcoming_birthdays:
                    print(f"{name}'s birthday on {birthday}")
            else:
                print("No upcoming birthdays.")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
