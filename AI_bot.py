from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import ReplyKeyboardMarkup as rkm

from Matches.Matches import Matches
from TTTGame.TTT import Game
from Big_xo.Big_xo import BigGame
from WolframAlpha_api.Wolfram import Wolfram
from search_engine.index import SearchEngine

from update2text import update2text


BOT_API_TOKEN = "496585400:AAHBJEfVNDTcu-pIVne_xuBUf8OW_womLwg"


main_menu = rkm([['tic-tac-toe'], ['5 in a row'], ['matches'], ['wolfram']], one_time_keyboard=True)

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
    text = update2text(update, BOT_API_TOKEN, "en_US")

    global search_engine




    global activity

    if activity == None:
        result, similarity = search_engine.find(text)

        if similarity<0.5:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text='{}!\nPlease, speak slowly and clearly'.format(
                    update.message.from_user.first_name),
                reply_markup=main_menu
            )
            return

        if result == 'tic-tac-toe':
            activity = Game()
        elif result == '5 in a row':
            activity = BigGame()
        elif result == 'matches':
            activity = Matches()
        elif result == 'wolfram':
            activity = Wolfram()

        activity.first_query(bot, update)



    elif text == 'Exit':  # EXIT sign sent from Game instance:
        activity = None
        start(bot, update)

    else:
        activity.process(text, bot, update)
        # Game will have user_id field


def handle_activity_choosing(text, user_session, bot_wrapper):
    global search_engine

    result, similarity = search_engine.find(text)

    if similarity < 0.5:
        # user_session['data']['handler'] = handlers['no_activity_found']
        return True
    else:
        # user_session['data']['handler'] = handlers[result]
        return True

    return result


# ------------------------ Init stuff --------------------

def init_search_engine():
    global search_engine
    facts = ['tic-tac-toe', '5 in a row', 'matches', 'wolfram']
    search_engine = SearchEngine(facts)

# --------------------------------------------------


def main():
    """Run bot."""
    global BOT_API_TOKEN

    updater = Updater(BOT_API_TOKEN)

    # loads model to create embeddings
    SearchEngine.load_model()
    # initing search engine
    init_search_engine()

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
