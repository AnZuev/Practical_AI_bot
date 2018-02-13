from ttt_game import board
from ttt_game import alpha_beta_prunning
from telegram import ReplyKeyboardMarkup as rkm


class Game:

    def __init__(self):
        self.board = board.Board()
        self.abp = alpha_beta_prunning.AlphaBetaPrunning()
        self.difficulty = 1
        self.wish = 'X'

    def start(self, bot, update):
        choice = rkm([["Easy"], ["Medium"], ["Hard"]])
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text="Select difficulty level:",
            reply_markup=choice
        )

    def difficulty(self, bot, update):
        if update.message.text == "Easy":
            self.difficulty = 1
        if update.message.text == "Medium":
            self.difficulty = 3
        if update.message.text == "Hard":
            self.difficulty = 9

        choice = rkm([['Sure!'], ['No, thanks']])
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text="Ok, " + update.message.text + "\nDo you want to play first?",
            reply_markup=choice
        )

    def order(self, bot, update):
        if update.message.text == 'No, thanks':
            self.wish = "O"
        else:
            self.wish = "X"
        self.__status(bot, update)
        self.__play(bot, update)

    def __play(self, bot, update):
        if self.board.get_turn().value == self.wish:
            choice = rkm([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']])
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="Your turn :)",
                reply_markup=choice
            )
        else:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="Well, my turn ... "
            )
            self.abp.run(self.board.get_turn(), self.board, self.difficulty)
            if self.board.get_turn().value == self.wish:
                self.__status(bot, update)
            if self.board.is_game_over():
                self.__print_winner(bot, update)
                self.__try_again_check(bot, update)
            else:
                self.__play(bot, update)

    def __status(self, bot, update):
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text=str(self.board)
        )

    def get_player_move(self, bot, update):
        val = int(update.message.text) - 1
        if not self.board.move(val):
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="The selected index must be blank, this one is already Occupied."
            )
        if self.board.get_turn().value == self.wish:
            self.__status(bot, update)
        if self.board.is_game_over():
            self.__print_winner(bot, update)
            self.__try_again_check(bot, update)
        else:
            self.__play(bot, update)

    def __print_winner(self, bot, update):
        winner = self.board.get_winner()
        if winner == board.State.Blank:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="Draw"
            )
        else:
            if winner.name == self.wish:
                bot.sendMessage(
                    chat_id=update.message.chat.id,
                    text="Well, you win!"
                )
            else:
                bot.sendMessage(
                    chat_id=update.message.chat.id,
                    text="Ha-ha! I win!"
                )
    def __try_again_check(self, bot, update):
        choice = rkm([['Yes!'], ['No']])
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text="Will play again?",
            reply_markup=choice
        )
