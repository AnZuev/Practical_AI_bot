from ttt_game import board
from ttt_game import alpha_beta_prunning
from telegram import ReplyKeyboardMarkup as rkm
from libs import BotWrapper
from enum import Enum


class Game:

    def __init__(self):
        self.board = board.Board()
        self.abp = alpha_beta_prunning.AlphaBetaPrunning()
        self.difficulty = 1
        self.wish = 'X'

    def start(self, bot_wrapper: BotWrapper, text: str):
        buttons = rkm([["Easy"], ["Medium"], ["Hard"]])
        bot_wrapper.send("Select difficulty level:", buttons)

    def set_difficulty(self, choice):
        if choice == "easy":
            self.difficulty = 1
        if choice == "medium":
            self.difficulty = 3
        if choice == "hard":
            self.difficulty = 9

    def choose_player_type(self, bot_wrapper: BotWrapper,  player_type: str):
        if player_type == 'o':
            self.wish = "O"
        else:
            self.wish = "X"

        self.__status(bot_wrapper)
        self.__play(bot_wrapper)

    def __play(self, bot_wrapper: BotWrapper, text: str):
        if self.board.get_turn().value == self.wish:
            buttons = rkm([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']])
            bot_wrapper.send("Your turn :)", buttons)
        else:
            bot_wrapper.send("Well, my turn ... ")

            self.abp.run(self.board.get_turn(), self.board, self.difficulty)
            if self.board.get_turn().value == self.wish:
                self.__status(bot_wrapper)
            if self.board.is_game_over():
                self.__print_winner(bot_wrapper)
            else:
                self.__play(bot_wrapper, text)

    def __status(self, bot_wrapper: BotWrapper):
        bot_wrapper.send(str(self.board))

    def get_player_move(self, bot_wrapper: BotWrapper, text: str):
        val = int(text) - 1
        if not self.board.move(val):
            bot_wrapper.send("The selected index must be blank, this one is already Occupied.")
        if self.board.get_turn().value == self.wish:
            self.__status(bot_wrapper)
        if self.board.is_game_over():
            self.__print_winner(bot_wrapper)
        else:
            self.__play(bot_wrapper, text)

    def __print_winner(self, bot_wrapper: BotWrapper):
        winner = self.board.get_winner()
        if winner == board.State.Blank:
            bot_wrapper.send("Draw")
        else:
            if winner.name == self.wish:
                bot_wrapper.send("Well, you win!")
            else:
                bot_wrapper.send("Ha-ha! I win!")


class State(Enum):
    not_started = 0,
    difficulty_choosing = 1,
    player_type_choosing = 2,
    playing = 3,
    finished = 4
