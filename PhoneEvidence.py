Phone_Evidence = {
    1111111111: "Amal",
    2222222222: "Mohammed",
    3333333333: "Khadijah",
    4444444444: "Abdullah",
    5555555555: "Rawan",
    6666666666: "Faisal",
    7777777777: "Layla",
}

import click

choices = ["search by name", "search by number", "add a person", "exit"]
print(
    """
1.search by name
2.search by number
3.add a person
4.exit'
"""
)

choice = click.prompt("Choose", type=int)
choice = choices[choice - 1]

if choice == "search by name":
    name = input("Enter name: ")
    for K, V in Phone_Evidence.items():
        if name == V:
            print(f"Phone number for {name} is {K}")

elif choice == "search by number":
    Except = False
    num = -1
    try:
        num = int(input("Enter Phone Number: "))
    except:
        Except = True

    if len(str(num)) == 10 and num not in Phone_Evidence.keys():
        print("Sorry, the number is not found ")
    elif len(str(num)) != 10 or Except:
        print("This is invalid number")

elif choice == "add a person":
    num = click.prompt("Enter a number: ", type=int)
    name = input("Enter name: ")
    if len(str(num)) != 10:
        print("number not equal 10")
    elif num not in Phone_Evidence.keys() and name not in Phone_Evidence.values():
        Phone_Evidence[num] = name
    else:
        print("there is same number or name")

else:
    pass
