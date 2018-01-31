from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup as rkm
from telegram import User

from WolframAlpha_api.AI_bot_search import ask
from Matches.Matches import Matches
from TTTGame.Game import Game
from Big_xo.game import *
from Big_xo.players import *


main_menu = rkm([['WolframAlpha search'], ['Matches'], ['Tic tac toe'], ['XO 5 in a row']], one_time_keyboard=True)
show_menu = rkm([['Choose another activity']])
users = {}


def start(bot, update):
    global users
    users[update.message.from_user.id] = {}
    users[update.message.from_user.id]['matches'] = Matches()
    users[update.message.from_user.id]['TTT'] = Game()
    bot.sendMessage(
        chat_id=update.message.chat.id,
        text='Hi, {}!\nI\'m glad to see you here.\nPlease, choose what you want to open.'.format(update.message.from_user.first_name),
        reply_markup=main_menu
    )


def handle_choice(bot, update):
    mes = update.message.text
    if mes == 'Choose another activity':
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text='Please, choose what you want to open.',
            reply_markup=main_menu
        )

    elif mes == 'WolframAlpha search':
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text='Nice!\nI can send a query to WolframAlpha search system for you.\nEnter some query below'
        )

    elif mes == 'Matches':
        handle_matches(bot, update)

    elif mes == 'Tic tac toe':
        handle_tic_tac_toe(bot, update)

    elif mes == 'XO 5 in a row':
        handle_XO5(bot, update)

    else:
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text='I can suggest you 4 activities, so please, choose one among them.',
            reply_markup=main_menu
        )


def handle_search(bot, update):
    bot.sendChatAction(
        chat_id=update.message.chat.id,
        action='typing'
    )

    subpods = ask(update.message.text)
    for pod in subpods:
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text=pod.plaintext.string
        )
    bot.sendMessage(
        chat_id=update.message.chat.id,
        text='You can enter and ask something else or exit',
        reply_markup=show_menu
    )


def handle_matches(bot, update):
    global users
    bot.sendMessage(
        chat_id=update.message.chat.id,
        text="Do you want to play first?",
        reply_markup=users[update.message.from_user.id]['matches'].start_choice
    )


def handle_tic_tac_toe(bot, update):
    global users
    users[update.message.from_user.id]['TTT'].start(bot, update)


def handle_XO5(bot, update):
    ai = AI("AI Player")
    human = Player("Human Player")
    g = BigGame(human, ai, bot, update, 10)



# Filters for button messages handling

class MenuFilter(filters.BaseFilter):
    def filter(self, message):
        if message.text == 'Search' or message.text == 'Matches' or message.text == 'Tic tac toe' or message.text == 'XO 5 in a row' or message.text == 'Choose another activity' or message.text == 'No' or message.text == 'Enough':
            return True
        else:
            return False


class DifficultyFilter(filters.BaseFilter):
    def filter(self, message):
        if message.text == "Easy" or message.text == "Medium" or message.text == "Hard":
            return True
        else:
            return False


class OrderFilter(filters.BaseFilter):
    def filter(self, message):
        if message.text == 'Sure!' or message.text == 'No, thanks':
            return True
        else:
            return False


class MatchesOrderFilter(filters.BaseFilter):
    def filter(self, message):
        if message.text == 'Yes, I start' or message.text == 'After you':
            return True
        else:
            return False


class MoveFilter(filters.BaseFilter):
    def filter(self, message):
        if message.text in "123456789":
            return True
        else:
            return False


class MatchesMoveFilter(filters.BaseFilter):
    def filter(self, message):
        if message.text == '1 match' or message.text == '2 matches' or message.text == '3 matches':
            return True
        else:
            return False


class StartAgainFilter(filters.BaseFilter):
    def filter(self, message):
        if message.text == 'Yes!':
            return True
        else:
            return False


class MatchesStartAgainFilter(filters.BaseFilter):
    def filter(self, message):
        if message.text == 'One more time!':
            return True
        else:
            return False


def difficulty(bot, update):
    global users
    users[update.message.from_user.id]['TTT'].difficulty(bot, update)

def order(bot, update):
    global users
    users[update.message.from_user.id]['TTT'].order(bot, update)

def getPlayerMove(bot, update):
    global users
    users[update.message.from_user.id]['TTT'].getPlayerMove(bot, update)

def matches_choice(bot, update):
    global users
    users[update.message.from_user.id]['matches'].matches_choice(bot, update)




def main():
    """Run bot."""
    #updater = Updater("496585400:AAHBJEfVNDTcu-pIVne_xuBUf8OW_womLwg")
    updater = Updater("337683580:AAGYNf_8C6Etcf-6uH0xqnd2DVMuguSgk6o")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))


    menu_filter_instance = MenuFilter()
    dp.add_handler(MessageHandler(menu_filter_instance, handle_choice))


    # Matches handler
    m_order_filter_instance = MatchesOrderFilter()
    dp.add_handler(MessageHandler(m_order_filter_instance, matches_choice))

    m_move_filter_instance = MatchesMoveFilter()
    dp.add_handler(MessageHandler(m_move_filter_instance, matches_choice))

    m_again_filter_instance = MatchesStartAgainFilter()
    dp.add_handler(MessageHandler(m_again_filter_instance, handle_matches))


    # Tic tac toe handlers
    diff_filter_instance = DifficultyFilter()
    dp.add_handler(MessageHandler(diff_filter_instance, difficulty))

    order_filter_instance = OrderFilter()
    dp.add_handler(MessageHandler(order_filter_instance, order))

    move_filter_instance = MoveFilter()
    dp.add_handler(MessageHandler(move_filter_instance, getPlayerMove))

    again_filter_instance = StartAgainFilter()
    dp.add_handler(MessageHandler(again_filter_instance, handle_tic_tac_toe))


    # WolframAlpha handler
    dp.add_handler(MessageHandler(filters.Filters.text, handle_search))


    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
