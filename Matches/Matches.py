# Использование:
# 1. Создать объект класса
# 2. Если человек ходит первый, то вызывать make_move() пока get_current_number > 0
# 3. Если бот ходит первый, то вызвать сначала respond_move(), далее как в п.2
# 4. При повторном использовании либо заного создать объект, либо вызвать restart()

import random
from telegram import ReplyKeyboardMarkup as rkm
from Activity import Activity



class Matches(Activity):


    def __init__(self):
        self.start_choice = rkm([['Yes, I start'], ['After you']])
        self.again_choice = rkm([['One more time!'], ['Exit']])
        self.three_choice = rkm([['1 match'], ['2 matches'], ['3 matches']])
        self.current_number = 21


    def first_query(self, bot, update):
        self.current_number = 21
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text="Do you want to play first?",
            reply_markup=self.start_choice
        )


    def process(self, query, bot, update):
        self.matches_choice(query, bot, update)


    def matches_choice(self, query, bot, update):
        if query == 'Yes, I start':
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="Choose how many matches to take",
                reply_markup=self.three_choice
            )
        elif query == 'After you':
            self.respond_move(bot, update)
        elif query == 'One more time!':
            self.first_query(bot, update)
        else:
            self.make_move(query[0], bot, update)


    def make_move(self, move, bot, update):

        move = int(move)

        if move < 1 or move > 3:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="Wrong move. You can only take 1, 2 or 3 matches"
            )

        elif self.currentNumber - move < 0:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="Wrong move. Can't take more than there currently are"
            )

        elif self.currentNumber == move:
            self.currentNumber = 0

            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="You lose!\nStart again?",
                reply_markup=self.again_choice
            )

        else:
            self.currentNumber -= move
            return self.respond_move(bot, update)


    def respond_move(self, bot, update):

        if self.currentNumber == 1:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="You win, congrats!\nStart again?",
                reply_markup=self.again_choice
            )
        else:
            answer = (self.currentNumber - 1) % 4

            if answer == 0:
                answer = random.randint(1, 3)

            self.currentNumber -= answer

            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="I take " + str(answer) + ". Current number of matches: " +
                str(self.get_current_number()) + "\nYour turn",
                reply_markup=self.three_choice
            )


    def get_current_number(self):
        return self.currentNumber


    def max_possible_move(self):
        return min(3, self.currentNumber)
