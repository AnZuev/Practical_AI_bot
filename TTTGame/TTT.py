`from Activity import Activity
from TTTGame import Board
from TTTGame import AlphaBetaPrunning
from telegram import ReplyKeyboardMarkup as rkm


class Game(Activity):

    def __init__(self):
        self.difficulty = None
        self.wish = None
        self.board = Board.Board()
        self.abp = AlphaBetaPrunning.AlphaBetaPrunning()

    def first_query(self, bot, update):
        self.__init__()
        self.start(bot, update)

    def process(self, query, bot, update):
        if query == 'Yes!':
            self.first_query(bot, update)

        elif self.difficulty == None:
            self.set_difficulty(query, bot, update)

        elif self.wish == None:
            self.order(query, bot, update)

        else:
            self.getPlayerMove(query, bot, update)


    def start(self, bot, update):
        choice = rkm([["Easy"], ["Medium"], ["Hard"]])
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text="Select difficulty level:",
            reply_markup=choice
        )


    def set_difficulty(self, query, bot, update):
        if query =="Easy":
            self.difficulty=1
        if query =="Medium":
            self.difficulty=3
        if query =="Hard":
            self.difficulty=9

        choice = rkm([['Sure!'], ['No, thanks']])
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text="Ok, " + query + "\nDo you want to play first?",
            reply_markup=choice
        )


    def order(self, query, bot, update):
        if query == 'No, thanks':
            self.wish="O"
        else:
            self.wish="X"
        self.__status(bot, update)
        self.__play(bot, update)


    def __play(self, bot, update):
        if self.board.getTurn().value == self.wish:
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
            self.abp.run(self.board.getTurn(), self.board, self.difficulty)
            if self.board.getTurn().value == self.wish:
                self.__status(bot, update)
            if self.board.isGameOver():
                self.__printWinner(bot, update)
                self.__tryAgainCheck(bot, update)
            else:
                self.__play(bot, update)


    def __status(self, bot, update):
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text=str(self.board)
        )


    def getPlayerMove(self, query, bot, update):
        val = int(query) - 1
        if not self.board.move(val):
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="The selected index must be blank, this one is already occupied."
            )

        if self.board.getTurn().value == self.wish:
            self.__status(bot, update)

        if self.board.isGameOver():
            self.__printWinner(bot, update)
            self.__tryAgainCheck(bot, update)
        else:
            self.__play(bot, update)


    def __printWinner(self, bot, update):
        winner = self.board.getWinner()
        if winner == Board.State.Blank:
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


    def __tryAgainCheck(self, bot, update):
        choice = rkm([['Yes!'], ['Exit']])
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text="Will play again?",
            reply_markup=choice
        )
