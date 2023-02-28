import datetime

DATA = {}

def check_name(name: str):
    if not name.isalpha() or len(name) < 5 or DATA.get(name):
        print("enter name with at least 5 ascii characters not entered already")
        return False
    return True

def check_date(birth_date:str):
    try:
        date = datetime.datetime.strptime(birth_date, '%d-%M-%Y')
    except ValueError as e:
        print("enter date in correct format")
        return None 
    return date

def input_data():
    while True:
        name = input('Enter name: ')
        birth_date = input('Enter birthdate in format dd-mm-yyyy: ')
        date = check_date(birth_date)
        if date and check_name(name):
            return {name: date}
     
def store_data(row):
    DATA.update(row)

def old_and_young():
    old = min(DATA, key=DATA.get)
    young = max(DATA, key=DATA.get)
    print(f"The oldest one is {old}")
    print(f"The youngest one is {young}")

def print_details():
    today = datetime.datetime.now()
    for name, date in DATA.items():
        age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
        print(f"{name} is {age} years old and she/he was born on {date.strftime('%A')}")
    old_and_young()
    print(f"total people is {len(DATA)}")

def main():
    while True:
        data = input_data()
        store_data(data)
        print("do you want to add more? ", end="")
        a = input("y or n: ")
        if a == "n":
            break
    print_details()

if __name__ == '__main__':
    main()
    
