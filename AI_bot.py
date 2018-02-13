from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import ReplyKeyboardMarkup as rkm

from matches.game import Game as MatchesGame
from ttt_game.ttt import Game as TTTGame
from big_xo.game import Game as BigXOGame
from wolfram_alpha_api import wolfram as Wolfram
from search_engine.index import SearchEngine


main_menu = rkm([['WolframAlpha search'], ['matches'], ['Tic tac toe'], ['XO 5 in a row']], one_time_keyboard=True)

# session
sessions = dict()

# search engine
search_engine = None

# handlers
handlers = dict()


# ------------------------ Bot Wrapper --------------------

class BotWrapper:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def send(self, message, buttons=None, audio_message=None):

        # any pre-processing could be inserted here (translating and so on)
        self.bot.send(
            chatid=self.chat_id,
            text=message,
            reply_markup=buttons
        )


# --------------------------------------------------


# ------------------------ Handlers --------------------


# handle command 'start'
def handle_start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat.id,
        text='Hi, {}!\nI\'m glad to see you here.\nPlease, say sending audiomessage'
             ' or choose below what you want to open.'.format(update.message.from_user.first_name),
        reply_markup=main_menu
    )


# each handler below has to return False if the state changing
# is required in order to end processing of the user input
def handle_message(bot, update):
    global sessions

    # TODO:  f(update) -> text
    text = update.message.text

    bot_wrapper = BotWrapper(bot, update.message.chat.id)
    user_id = update.message.from_user.id
    user_session = sessions.get(user_id, dict({'data': dict(), 'id': user_id, 'handler': handlers['default']}))

    while True:
        handler_result = user_session['handler'](text, user_session, bot_wrapper)
        if not handler_result:
            break

    sessions[user_id] = user_session


def handle_ttt_game(text, user_session, bot_wrapper):
    pass
    return False


def handle_big_xo_game(text, user_session, bot_wrapper):
    pass
    return False


def handle_matches_game(text, user_session, bot_wrapper):
    pass
    return False


def handle_wolfram(text, user_session, bot_wrapper):
    pass


def handle_no_activity_found(text, user_session, bot_wrapper: BotWrapper):
    text = "Sorry, I don't understand the activity you want to start. Here is the list below :)"
    bot_wrapper.send(text, main_menu)
    return False


def handle_activity_choosing(text, user_session, bot_wrapper):
    global search_engine
    global handlers

    result, similarity = search_engine.find(text)

    if similarity < 0.5:
        user_session['data']['handler'] = handlers['no_activity_found']
        return True
    else:
        user_session['data']['handler'] = handlers[result]
        return True

# --------------------------------------------------


# ------------------------ Init stuff --------------------

def init_search_engine():
    global search_engine
    facts = ['tic-tac-toe', '5 in a row', 'matches', 'wolfram']
    search_engine = SearchEngine(facts)


def init_handlers():
    global handlers
    handlers['tic-tac-toe'] = handle_ttt_game
    handlers['5 in a row'] = handle_big_xo_game
    handlers['matches'] = handle_matches_game
    handlers['wolfram'] = handle_wolfram
    handlers['default'] = handle_activity_choosing
    handlers['no_activity_found'] = handle_no_activity_found

# --------------------------------------------------


def main():
    """Run bot."""
    updater = Updater("496585400:AAHBJEfVNDTcu-pIVne_xuBUf8OW_womLwg")

    # loads model to create embeddings
    SearchEngine.load_model()

    init_search_engine()
    init_handlers()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", handle_start))

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

