
# quiz app
import json 
import click 

class Quiz:

    QUIZ_TOTAL_SCORE = 10

    def __init__(self):
        self.__data = self.load_json()
        self.__question_number = 0
        self.__quiz_score = 0

    def load_json(self) -> dict:
        with open('questions.json', 'r') as f:
            return json.load(f)

    def get_quiz_total_score(self) -> int:
        return self.__data['total_score']
    
    def get_total_questions(self) -> int:
        return self.__data['total_questions']

    def set_question_number(self, question_number:int) -> None:
        self.__question_number = question_number

    def set_quiz_score(self, score:int) -> None:
        self.__quiz_score = score

    def get_quiz_score(self) -> int:
        return self.__quiz_score

    def quiz_score_percentage(self) -> float:
        return self.get_quiz_score() / self.get_quiz_total_score() * 100

    def get_question(self) -> dict:
        return self.__data['questions'][self.__question_number]['question']

    def get_choices(self) -> list:
        return self.__data['questions'][self.__question_number]['choices']

    def get_corrct_answer(self) -> str:
        return self.__data['questions'][self.__question_number]['correct_answer']

    def get_question_score(self) -> int:
        return self.__data['questions'][self.__question_number]['score']



def play():

    quiz_app = Quiz()
    print('start quiz')
    print('----------------------------------------------------')
    print(f'you have to complete {quiz_app.get_total_questions()} questions')

    for question_number in range(quiz_app.get_total_questions()):
        print('----------------------------------------------------')
        quiz_app.set_question_number(question_number)
        print(f'question {question_number + 1}: ', end='')
        print(quiz_app.get_question())
        
        print('\n')
        for num, choice in enumerate(quiz_app.get_choices() , 1):
            print(f'{num}. {choice}')
        print('\n')
        
        answer = click.prompt('your answer: ', type=click.Choice(list(str(n) for n in range(1, len(quiz_app.get_choices())+1))))
        if quiz_app.get_choices()[int(answer)-1] == quiz_app.get_corrct_answer():
            quiz_app.set_quiz_score(quiz_app.get_quiz_score() + quiz_app.get_question_score())
            print('correct answer')
        else:
            print('wrong answer')

    print('----------------------------------------------------')
    print(f'your score is {quiz_app.get_quiz_score()}')
    print(f'your score percentage is {quiz_app.quiz_score_percentage()}')
    print('----------------------------------------------------')

def main():
    play()

if __name__ == '__main__':
    print("Welcome to Quiz App")
    print("===================")
    print("1. Play")
    print("2. Exit")
    print("===================")
    choice = click.prompt("Enter your choice: ", type=click.Choice(['1', '2']))
    if int(choice) == 1:
        main()
    else:
        print("Bye")
        exit()
