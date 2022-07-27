
class Course:
    list_ids, list_names = [],[]
    
    twoDArray = [["" for i in range(7)] for i in range(5)]
    BookedTime = {
        'Beginner':twoDArray,
        'Intermediate':twoDArray,
        'Advanced':twoDArray
    }
    LevelCourses = {
        'Beginner':[],
        'Intermediate':[],
        'Advanced':[]
    }
    def __init__(self, CId:int, CName:str, CPrice:int, CLevel:str, Chours:int) -> None:
        
        __class__.list_ids.append(CId)
        __class__.list_names.append(CName)
        self.id = CId
        self.name = CName
        self.price = CPrice
        self.level = CLevel
        self.hours = Chours
        __class__.LevelCourses[CLevel].append(self)


    def getId(self)->int:
        return self.id
    
    def getName(self)->str:
        return self.name
    
    def getPrice(self)->int:
        return self.price
    
    def getLevel(self)->str:
        return self.level

    def setTime(day:int, hour:int, level:str, name:str):
        __class__.BookedTime[level][day-1][hour-1] = name

    def is_Set_Time(day:int, hour:int, level:str):
        return bool(__class__.BookedTime[level][day-1][hour-1])

    def is_Unique_Id(cid:int)->bool:
        return not cid in __class__.list_ids
    
    def is_Unique_Name(name:str)->bool:
        return not name.casefold() in __class__.list_names

    def getCourse(level:str, ID:int):
        for course in __class__.LevelCourses[level]:
            if course.getId() == ID:
                return course


class Student:
    list_ids = []
    Registered_Students = []
    def __init__(self, Std_Id:int, Std_Name:str, Std_Level:str, Std_Wallet:int) -> None:
        self.id = Std_Id
        __class__.list_ids.append(Std_Id)
        self.name = Std_Name
        self.level = Std_Level
        self.wallet = Std_Wallet
        self.Std_Course_List = []
        __class__.Registered_Students.append(self)

    def getId(self)->str:
        return self.id

    def getName(self)->str:
        return self.name

    def getLevel(self)->str:
        return self.level

    def setWallet(self, wallet):
        self.wallet = wallet

    def getWallet(self)->int:
        return self.wallet
    
    added_courses_ids = []
    added_courses_names = []
    
    def add_Course(self, course:Course):
        __class__.added_courses_ids.append(course.getId())
        __class__.added_courses_names.append(course.getName())
        self.Std_Course_List.append(course)
        
    def getSchedule(self):
        schedule = Course.BookedTime[self.getLevel()]
        for i in range(5):
            for j in range(7):
                if schedule[i][j] and schedule[i][j] not in __class__.added_courses_names:
                    schedule[i][j] = ''
        return schedule
    
    def deleteCourse(self, course:Course):
        __class__.added_courses_ids.remove(course.getId())
        __class__.added_courses_names.remove(course.getName())
        self.Std_Course_List.remove(course)
    
    def is_Unique_Id(sid:int)->bool:
        return not sid in __class__.list_ids

    def isBookedCourse(self, ID:int)->bool:
        for course in self.Std_Course_List:
            if course.getId() == ID:
                return True
        return False

    def getStudent(ID:int):
        for student in __class__.Registered_Students:
            if student.getId() == ID:
                return student
