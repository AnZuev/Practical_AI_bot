from enum import Enum
from copy import deepcopy


class State(Enum):
    Blank = "-"
    X = "X"
    O = "O"


class Board:
    def __init__(self):
        self.BOARD_SIDE = 3
        self.winner = State.Blank
        self.player_turn = State.X
        self.avaliable_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.board = [[State.Blank for j in range(self.BOARD_SIDE)] for i in range(self.BOARD_SIDE)]
        self.move_counter = 0
        self.game_over = False

    def move(self, index):
        return self.__move(index % self.BOARD_SIDE, index // self.BOARD_SIDE)

    def reset(self):
        self.BOARD_SIDE = 3
        self.winner = State.Blank
        self.player_turn = State.X
        self.avaliable_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.board = [[State.Blank for j in range(self.BOARD_SIDE)] for i in range(self.BOARD_SIDE)]
        self.move_counter = 0
        self.game_over = False

    def __move(self, x, y):
        if self.game_over:
            return False
        if self.board[y][x] == State.Blank:
            self.board[y][x] = self.player_turn
        else:
            return False
        self.move_counter += 1
        self.avaliable_moves.remove(y * self.BOARD_SIDE + x)
        if self.move_counter == self.BOARD_SIDE ** 2:
                self.winner = State.Blank;
                self.game_over = True;
        self.__check_row(y)
        self.__check_column(x)
        self.____check_diagonal_from_top_left(x, y)
        self.____check_diagonal_from_top_right(x, y)

        self.player_turn = State.O if self.player_turn == State.X else State.X
        return True

    def is_game_over(self):
        return self.game_over

    def get_turn(self):
        return self.player_turn

    def get_winner(self):
        if self.is_game_over():
            return self.winner

    def get_avaliable_moves(self):
        return self.avaliable_moves

    def copy(self):
        new_board = Board()
        new_board.board = deepcopy(self.board)
        new_board.player_turn = self.player_turn
        new_board.winner = self.winner
        new_board.move_counter = self.move_counter
        new_board.game_over = self.game_over
        new_board.avaliable_moves = deepcopy(self.avaliable_moves)
        return new_board

    def __str__(self):
        ans = ""
        for j in self.board:
            for i in j:
                ans += " ".join(i.value) + " "
            ans += "\n"
        return ans

    def __check_row(self, row):
        for i in range(1, self.BOARD_SIDE):
            if self.board[row][i] != self.board[row][i - 1]:
                break
            if i == self.BOARD_SIDE - 1:
                self.winner = self.player_turn
                self.game_over = True

    def __check_column(self, column):
        for i in range(1, self.BOARD_SIDE):
            if self.board[i][column] != self.board[i - 1][column]:
                break
            if i == self.BOARD_SIDE - 1:
                self.winner = self.player_turn
                self.game_over = True

    def ____check_diagonal_from_top_left(self, x, y):
        if x == y:
            for i in range(1, self.BOARD_SIDE):
                if self.board[i][i] != self.board[i - 1][i - 1]:
                    break
                if i == self.BOARD_SIDE - 1:
                    self.winner = self.player_turn
                    self.game_over = True

    def ____check_diagonal_from_top_right(self, x, y):
        if (self.BOARD_SIDE - 1 - x) == y:
            for i in range(1, self.BOARD_SIDE):
                if self.board[self.BOARD_SIDE - 1 - i][i] != self.board[self.BOARD_SIDE - i][i - 1]:
                    break
                if i == self.BOARD_SIDE - 1:
                    self.winner = self.player_turn
                    self.game_over = True
