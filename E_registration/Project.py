from Classes import Student, Course
import click
from tabulate import tabulate


def CheckID(ID: int, Class: object):
    while True:
        if len(str(ID)) != 4:
            print("Id must be 4 digits")
            ID = click.prompt("Enter Id", type=int)
            continue
        if not Class.is_Unique_Id(ID):
            print("Id is already exited")
            ID = click.prompt("Enter Id", type=int)
            continue
        return ID


def choosenStudent() -> Student:
    print("\nRegistered Studentd:\n")
    for c, ID in enumerate(Student.list_ids):
        student = Student.getStudent(ID)
        print(c + 1, ".", ID, " ", student.getName(), " ", student.getLevel())

    ID = int(
        click.prompt(
            "\nChoose student ID", type=click.Choice([str(i) for i in Student.list_ids])
        )
    )
    return Student.getStudent(ID)


def chosen_course_to_be_booked(chosen_student) -> Course:
    print("\nRegistered Courses:\n")
    for c, course in enumerate(Course.LevelCourses[chosen_student.getLevel()]):
        print(c + 1, ".", course.getId(), " ", course.getName(), " ", course.getPrice())

    ID = int(
        click.prompt(
            "\nChoose course ID", type=click.Choice([str(i) for i in Course.list_ids])
        )
    )
    return Course.getCourse(chosen_student.getLevel(), ID)


Levels = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
Days = ["1. Sunday", "2. Monday", "3. Tuesday", "4. Wednesday", "5. Thursday"]
nums = [8, 9, 10, 11, 12, 1, 2, 3]
Hours = [str(nums[x]) + "-" + str(nums[x + 1]) for x in range(len(nums) - 1)]

while True:

    Choices = [
        "1.Register new student",
        "2.Register new course",
        "3.Register course for student",
        "4.Delete course for student",
        "Print student schedule",
        "6.Exit system",
    ]
    print("\n".join(Choices))
    response = int(
        click.prompt(
            "choose ", type=click.Choice([str(x) for x in range(1, len(Choices) + 1)])
        )
    )

    if response == 1:
        SId = click.prompt("\nEnter Student Id with 4 digits", type=int)
        SId = CheckID(SId, Student)

        name = input("\nEnter Student name: ")

        print("\nchoose level:\n" + "\n".join(Levels.values()))
        levnum = int(
            click.prompt(
                "choose ",
                type=click.Choice([str(x) for x in range(1, len(Levels.keys()) + 1)]),
            )
        )
        level = Levels[levnum]

        wallet = click.prompt("\nEnter Student Wallet", type=int)

        Student(SId, name, level, wallet)

        print("\nStudent added successfully\n")

    elif response == 2:
        CId = click.prompt("\nEnter Course Id with 4 digits", type=int)
        CId = CheckID(CId, Course)

        while True:
            name = input("\nEnter Course Name: ")
            if Course.is_Unique_Name(name):
                break
            print("name is already existed")

        print("\nChoose level:\n" + "\n".join(Levels.values()))
        levnum = int(
            click.prompt(
                "Choose ",
                type=click.Choice([str(x) for x in range(1, len(Levels.keys()) + 1)]),
            )
        )
        level = Levels[levnum]

        price = click.prompt("\nEnter Course price", type=int)

        hours = click.prompt("\nEnter Course hours", type=int)

        Course(CId, name, price, level, hours)

        for hour in range(1, hours + 1):
            while True:
                print("\nChoose day for lecture ", hour, "of this course")
                print("\nDays:\n" + "\n".join(Days))
                book_day = int(
                    click.prompt(
                        "choose ",
                        type=click.Choice([str(x) for x in range(1, len(Days) + 1)]),
                    )
                )

                print("\nChoose time for lecture ", hour, "of this course")
                print("\nTimes:\n" + "\n".join(Hours))
                book_hour = int(
                    click.prompt(
                        "choose ",
                        type=click.Choice([str(x) for x in range(1, len(Hours) + 1)]),
                    )
                )
                if not Course.is_Set_Time(book_day, book_hour, level):
                    break
                print("\nthis time is already booked")
            Course.setTime(day=book_day, hour=book_hour, level=level, name=name)

        print("\nCourse added successfully\n")

    elif response == 3:
        if not Student.Registered_Students:
            print("\nthere are no registered students\n")
            continue

        chosen_student = choosenStudent()

        if not Course.LevelCourses[chosen_student.getLevel()]:
            print(
                "\nthers are no courses for this student level yet, please Register courses"
            )
            continue

        chosen_course = chosen_course_to_be_booked(chosen_student)

        if chosen_student.isBookedCourse(chosen_course.getId()):
            print("\nthis course is already sdded for this student\n")
            continue

        if chosen_student.getWallet() < chosen_course.getPrice():
            print("\nstudent wallet is not enough, so can not buy course\n")
            continue

        chosen_student.add_Course(chosen_course)
        print(
            "\n",
            chosen_course.getName(),
            " course is added successfully for student ",
            chosen_student.getName(),
            "\n",
        )

        price = chosen_course.getPrice()
        chosen_student.setWallet(chosen_student.getWallet() - price)
        print("\nstudent wallet becomes ", chosen_student.getWallet(), "\n")

    elif response == 4:
        if not Student.Registered_Students:
            print("\nthere are no registered students\n")
            continue

        chosen_student = choosenStudent()

        if not chosen_student.Std_Course_List:
            print("\nthere are no courses added for this student\n")
            continue

        print("\ncourses added to this student:")
        for c, course in enumerate(chosen_student.Std_Course_List):
            print(c + 1, ".", course.getId(), " ", course.getName())

        ID = int(
            click.prompt(
                "\nChoose course ID",
                type=click.Choice([str(i) for i in Student.added_courses_ids]),
            )
        )
        chosen_course = Course.getCourse(ID=ID, level=chosen_student.getLevel())

        price = chosen_course.getPrice()
        chosen_student.setWallet(chosen_student.getWallet() + price)
        print("\nstudent wallet becomes ", chosen_student.getWallet())

        chosen_student.deleteCourse(chosen_course)
        print(
            "\ncourse ",
            chosen_course.getName(),
            " is deleted for student ",
            chosen_student.getName(),
            "\n",
        )

    elif response == 5:
        if not Student.Registered_Students:
            print("\nthere are no registered students\n")
            continue

        chosen_student = choosenStudent()

        if not chosen_student.Std_Course_List:
            print("\nthere are no courses added for this student\n")
            continue

        schedule = chosen_student.getSchedule()
        schedule.insert(0, Hours)
        table = tabulate(
            schedule, headers="firstrow", tablefmt="fancy_grid", showindex=Days
        )
        print(table)

    else:
        print("system exited")
        exit(0)
