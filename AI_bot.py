from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import ReplyKeyboardMarkup as rkm

from Matches import Matches
from TTTGame import TTT
from Big_xo import Big_xo
from WolframAlpha_api import Wolfram
from search_engine.index import SearchEngine

from update2text import update2text


main_menu = rkm([['WolframAlpha search'], ['Matches'], ['Tic tac toe'], ['XO 5 in a row']], one_time_keyboard=True)

activity = None
# search engine
search_engine = None


def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat.id,
        text='Hi, {}!\nI\'m glad to see you here.\nPlease, say sending audiomessage or choose below what you want to open.'.format(update.message.from_user.first_name),
        reply_markup=main_menu
    )


def handle_message(bot, update):
    text = update2text(bot,update)


    global activity

    if activity == None:
        
        pass # TODO: f(text) -> choose game (globalHandler)
             # Game =

    elif text == 'Exit':  # EXIT sign sent from Game instance:
        activity = None
        start(bot, update)

    else:
        activity.process(bot, update, text)
        # Game will have user_id field


# ------------------------ Init stuff --------------------

def init_search_engine():
    global search_engine
    facts = ['tic-tac-toe', '5 in a row', 'matches', 'wolfram']
    search_engine = SearchEngine(facts)

# --------------------------------------------------


def main():
    """Run bot."""
    updater = Updater("496585400:AAHBJEfVNDTcu-pIVne_xuBUf8OW_womLwg")

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

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
