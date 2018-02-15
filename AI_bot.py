from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import ReplyKeyboardMarkup as rkm

from Matches.Matches import Matches
from TTTGame.TTT import Game
from Big_xo.Big_xo import BigGame
from WolframAlpha_api.Wolfram import Wolfram
#from search_engine.index import SearchEngine

from update2text import update2text


BOT_API_TOKEN = "496585400:AAHBJEfVNDTcu-pIVne_xuBUf8OW_womLwg"
#search_engine = None
users = {}


main_menu = rkm([['tic-tac-toe'], ['5 in a row'], ['matches'], ['wolfram']], one_time_keyboard=True)


def start(bot, update):
    global users
    print("Start for user", str(update.message.from_user.id))
    users[update.message.from_user.id] = {}
    users[update.message.from_user.id]['activity'] = None
    users[update.message.from_user.id]['text'] = None

    bot.sendMessage(
        chat_id=update.message.chat.id,
        text='Hi, {}!\nI\'m glad to see you here.\nPlease, say sending audiomessage or choose below what you want to open.'.format(update.message.from_user.first_name),
        reply_markup=main_menu
    )


def show_choice(bot, update, choice):
    bot.sendMessage(
        chat_id=update.message.chat.id,
        text='Ok, {}.\nExecuting {})'.format(update.message.from_user.first_name, choice)
    )


def handle_message(bot, update):
    global search_engine
    global users

    users[update.message.from_user.id]['text'] = update2text(update, BOT_API_TOKEN, "en_US")

    if users[update.message.from_user.id]['activity'] == None:
#        result, similarity = search_engine.find(users[update.message.from_user.id]['text'])
        result, similarity = users[update.message.from_user.id]['text'], 1

        if similarity<0.5:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text='I didn\'t understand you, {}!\nPlease, speak slowly and clearly'.format(
                    update.message.from_user.first_name),
                reply_markup=main_menu
            )

        elif result == 'tic-tac-toe':
            users[update.message.from_user.id]['activity'] = Game()
            show_choice(bot, update, 'tic-tac-toe')

        elif result == '5 in a row':
            users[update.message.from_user.id]['activity'] = BigGame()
            show_choice(bot, update, '5 in a row')

        elif result == 'matches':
            users[update.message.from_user.id]['activity'] = Matches()
            show_choice(bot, update, 'matches')

        elif result == 'wolfram':
            users[update.message.from_user.id]['activity'] = Wolfram()
            show_choice(bot, update, 'WolframAlpha')

        users[update.message.from_user.id]['activity'].first_query(bot, update)

    elif users[update.message.from_user.id]['text'] == 'Exit':
        users[update.message.from_user.id]['activity'] = None
        start(bot, update)

    else:
        users[update.message.from_user.id]['activity'].process(users[update.message.from_user.id]['text'], bot, update)


# ------------------------ Init stuff --------------------

# def init_search_engine():
#     global search_engine
#     facts = ['tic-tac-toe', '5 in a row', 'matches', 'wolfram']
#     search_engine = SearchEngine(facts)

# --------------------------------------------------


def main():
    """Run bot."""
    global BOT_API_TOKEN
    updater = Updater(BOT_API_TOKEN)

    # loads model to create embeddings
    #SearchEngine.load_model()
    # initing search engine
    #init_search_engine()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # handle all messages
    dp.add_handler(MessageHandler(Filters.all, handle_message))

    # Start the Bot
    updater.start_polling()

    print("Bot started")

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
