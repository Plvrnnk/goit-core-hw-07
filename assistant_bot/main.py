from bot_commands import * 

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def main():
    book = AddressBook()
    print("Welcome! I'm your assistant bot-helper.")
    print(command_list())
    while True:
        user_input = input('Enter your command: ')
        command, *args = parse_input(user_input)
        if command in ['exit', 'close']:
            print('Bye!')
            break
        elif command == 'hello':
            print(hello())
        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'phone':
            print(phone(args, book))
        elif command == 'all':
            print(show_all(book))
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(args, book))
        elif command == 'birthdays':
            print(birthdays(book))
        elif command == 'commands':
            print(command_list())
        else:
            print('Invalid command')

if __name__ == '__main__':
    main()