import requests
import os, random 

def download_file(url:str):
    if not os.path.exists('sowpods.txt'):
        r = requests.get(url=url)
        with open('sowpods.txt', 'w') as f:
            f.write(r.text) 

def get_data_from_file(filename: str) -> list[str]:
    with open(filename) as f:
        lines = f.readlines()
    return lines

def pick_word(lines: list[str]) -> str:
    return random.choice(lines).strip()


def enter_a_letter():
    letter = input('enter a letter:')
    if not letter or len(letter) > 1:
        print('not just a letter')
        return enter_a_letter()
    return letter 


def pattern_where_letter_in_word(word:str, guessed:list) -> str:
    pattern = list('_' * len(word))
    for i, l in enumerate(word):
        if l in guessed:
            pattern[i] = l

    return ''.join(pattern)

def is_guessed_letter(letter: str, guessed: list) -> bool:
    return letter in guessed

def guessing_game(word: str):
        
    TOTAL_INCORRECT_GUESSES = 6
    incorrect_guesses = 0
    guessed = []

    while True:

        letter = enter_a_letter()

        if not letter in word:
            print('incorrect!')
            incorrect_guesses += 1
            if incorrect_guesses == TOTAL_INCORRECT_GUESSES:
                print('you exceeds the your allowed number of incorrect guesses')
                exit()
            print(f'you have {TOTAL_INCORRECT_GUESSES - incorrect_guesses} incorrect guesses left')
            continue 

        if is_guessed_letter(letter, guessed):
            print('you already guessed this letter')
            continue

        guessed.append(letter)
        pattern = pattern_where_letter_in_word(word, guessed)
        print(f'you cover {pattern} of the word')

        if pattern == word:
            print('you won!')
            exit()


def main():
    download_file('http://norvig.com/ngrams/sowpods.txt')
    lines = get_data_from_file('sowpods.txt')
    word = pick_word(lines).strip().lower()
    print(f'you have to guess the word: {word}')
    guessing_game(word)
    
if __name__ == '__main__':
    main()
