from collections import UserDict
from datetime import datetime, date, timedelta
import re

class Field: # Base class for record fields.
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field): # For storing contact name
    def __init__(self, value):
        super().__init__(value)
        
class Phone(Field): # For storing contact phone numbers
    def __init__(self, value):
        super().__init__(value)
        if len(value) != 10:
            raise ValueError('Your phone does not meet requirements. Must be 10 numbers')
        
    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.value == other.value
        return False

class Birthday(Field): # For storing birhday info and converting data into datetime
    def __init__(self, value):
        try:
            if re.match(r"^\d{2}\.\d{2}\.\d{4}$", value):
                self.value = datetime.strptime(value,"%d.%m.%Y").date()
                # for val in value.split('.'):
                    # self.value = datetime.date(val[2], val[1], val[0])
        except ValueError:
            raise ValueError("Invalid date format. Try DD.MM.YYYY")
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
class Record: # For storing contact information, including name and phone list.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_phone(self, phone):
        phone = Phone(phone)
        if phone not in self.phones:
            self.phones.append(phone)
        return self.phones
    
    def remove_phone(self, phone):
        i = self.find_phone(Phone(phone).value)
        if i:
            self.phones.remove(i)
        else: raise ValueError("Phone is not found. Can't remove phone.")
        
    def edit_phone(self, phone, new_phone: str):
        i = self.find_phone(phone)
        if i:
            self.add_phone(new_phone)
            self.remove_phone(phone)
        else: raise ValueError('Phone is not found.')
              
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        else: return None
        
    def add_birtday(self, value):
        if self.birthday == None:
            self.birthday = Birthday(value)
        else: raise ValueError('Birtday is already added.')
           
    def __str__(self) -> str:
        return (f"Contact name: {self.name.value}, phones: {[p.value for p in self.phones]}, birthday: {self.birthday}")

class AddressBook(UserDict): # For storing and managing records.
    def add_record(self, record: Record):
        if record not in self.data:
            self.data[record.name.value] = record
            return 'Record is successfully added.'
        else: return 'Record is already added.'
    
    def find(self, found_name: str):
        if found_name in self.data:
            return self.data.get(found_name)
        else: return None
        
    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
            return 'Record was successfully deleted.'
        else: return 'There is no record for this name.'
    
    def __str__(self):
        return '\n'.join(f"Contact name: {recordname}, phones: {recordphone}, birthday: {recordbirthday}" for recordname, recordphone, recordbirthday in self.data.items())
    
    def find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)
    
    def adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday
    
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()
        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value
                birthday_this_year = birthday_date.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_date.replace(year= today.year + 1)
                    
            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = self.adjust_for_weekend(birthday_this_year)
                congratulation_date_str = datetime.strftime(birthday_this_year, "%d.%m.%Y")
                upcoming_birthdays.append({"name": record.name.value, "congratulation_date": congratulation_date_str})
        return upcoming_birthdays