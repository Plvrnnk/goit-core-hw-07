from contact_book import *

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'Give me name and phone please.'
        except KeyError:
            return 'Name does not exist! Try again please.'
        except IndexError:
            return 'Enter the argument for the command. Try again please.'
        except AttributeError:
            return 'Attributes are wrong! Try again please.'
        except Exception as e:
            return f'{e}! Try again!'
    return inner

# @input_error
def hello():
    return 'How can I help you?'

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, phone, new_phone, *_ = args
    record = book.find(name)
    message = "Contact changed."
    if record is None:
        message = 'Contact is not found'
    if record:
        record.edit_phone(phone, new_phone)
    return message

@input_error 
def phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        message = 'Contact is not found'
    else:
        message = f"{name}'s phone are: {' '.join([str(i) for i in record.phones])}"
    return message

@input_error 
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = 'Birthday is added.'
    if record is None:
        message = 'Contact is not found'
    else:
        
        record.add_birtday(birthday)
    return message

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        message = 'Contact is not found'
    else:
        message = f"{name}'s birthday is {record.birthday}"
    return message
    
@input_error
def birthdays(book: AddressBook):
    info = book.get_upcoming_birthdays()
    if not info:
        return 'No upcomming birthdays!'
    else: return info

# @input_error 
def show_all(book: AddressBook):
    return f'Contacts:\n{[str(i) for i in book.data.values()]}'

# @input_error
def command_list():
    return 'List of commands:\n1.hello\n2.add (username) (phone)\n3.change (username) (old phone) (new phone)\n4.phone (username)\n5.all\n6.add-birthday (name) (birthday date)\n7.show-birthday (name)\n8.birthdays\n9.commands\n10.close or exit'