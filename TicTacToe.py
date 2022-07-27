from time import sleep
from tabulate import tabulate


class TicTacToe:

    def __init__(self):
        self.board = None
        self.current_player = None
        self.winner = None

    def create_board(self):
        self.board = [[' '] * 3 for _ in range(3)]

    def print_board(self):
        print('the board: ')
        print(tabulate(self.board, tablefmt='grid'))

    def cell_filled(self, row, col):
        return self.board[row][col] != ' '

    def set_player(self, player):
        self.current_player = player

    def get_player(self):
        return self.current_player

    player = property(get_player, set_player)

    def fill_cell(self, row, col):
        self.board[row][col] = self.current_player  

    def check_winner(self):
        # check rows
        for row in self.board:
            if row[0] == row[1] == row[2] == self.current_player:
                self.winner = row[0]
                return True
        # check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.current_player:
                self.winner = self.board[0][col]
                return True
        # check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player:
            self.winner = self.board[0][0]
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player:
            self.winner = self.board[0][2]
            return True
        return False


def init_game():
    print('welcome to tic tac toe game...')
    game = TicTacToe()
    return game 


def set_player(game: TicTacToe, player):
    game.player = player


def change_player(game: TicTacToe):
    print(f'player {game.player} is done')
    if game.player == 'X':
        game.player = 'O'
        return
    game.player = 'X'


def first_player():
    players = ['X', 'O']
    while True:
        player = input(f'choose first player from {players}: ')
        if player not in players:
            print('wrong choice!')
            continue
        return player


def choose_from_range(rng):
    rng = list(str(x) for x in range(1, rng+1))
    while True:
        chosen = input(f'from {rng}:')
        if chosen not in rng:
            print('wrong choice!')
            continue
        return int(chosen)


def choose_position():
    print('enter row ', end="")
    row = choose_from_range(3)
    print('enter column ', end="")
    col = choose_from_range(3)
    return row-1, col-1


def play():

    MAX_NUM_OF_OCCURENCES = 9
    count_of_occurences = 0
    MIN_NUM_TO_CHECK_WINNER = 5

    game = init_game()
    game.create_board()
    sleep(5)

    player_to_play_first = first_player()
    game.player = player_to_play_first
    print(f'{player_to_play_first} will play first')

    print('start playing...')
    sleep(2)
    game.print_board()

    while True:
        
        count_of_occurences += 1

        print(f'for player {game.player}')
        row, col = choose_position()
        if game.cell_filled(row, col):
            print('this cell is already filled, try again')
            continue

        game.fill_cell(row, col)
        game.print_board()

        if count_of_occurences >= MIN_NUM_TO_CHECK_WINNER:
            if game.check_winner():
                print(f'player {game.player} won!')
                break

        if count_of_occurences == MAX_NUM_OF_OCCURENCES:
            print('no one is winner')
            break
        
        change_player(game)


if __name__ == '__main__':
    play()
