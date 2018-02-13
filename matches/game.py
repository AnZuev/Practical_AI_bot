import random
from telegram import ReplyKeyboardMarkup as rkm


# Использование:
# 1. Создать объект класса
# 2. Если человек ходит первый, то вызывать функцию makeMove пока getCurrentNumber>0
# 3. Если бот ходит первый, то вызвать сначала функцию respondMove, далее как в п.2
# 4. При повторном использовании либо заного создать объект, либо вызвать функцию restart

class Game(object):

    def __init__(self):
        self.currentNumber = 21
        self.start_choice = rkm([['Yes, I start'], ['After you']])
        self.again_choice = rkm([['One more time!'], ['Enough']])
        self.three_choice = rkm([['1 match'], ['2 matches'], ['3 matches']])

    def matches_choice(self, bot, update):
        if update.message.text == 'Yes, I start':
            msg = bot.sendMessage(
                chat_id=update.message.chat.id,
                text="Choose how many matches to take",
                reply_markup=self.three_choice
            )
        elif update.message.text == 'After you':
            self.respond_move(bot, update)
        else:
            self.make_move(update.message.text[0], bot, update)

    def make_move(self, move, bot, update):

        move = int(move)

        if move < 1 or move > 3:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="Wrong move. You can only take 1, 2 or 3 matches"
            )

        elif self.currentNumber-move < 0:
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
            rem = (self.currentNumber-1) % 4

            answer = rem

            if rem == 0:
                answer = random.randint(1, 3)

            self.currentNumber -= answer

            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="I take {}. Current number of matches: {}\n Your turn".format(str(answer), str(self.get_current_number())),
                reply_markup=self.three_choice
            )

    def get_current_number(self):
        return self.currentNumber

    def max_possible_move(self):
        return min(3, self.currentNumber)