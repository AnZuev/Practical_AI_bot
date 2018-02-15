from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import ReplyKeyboardMarkup as rkm

from libs import Session, BotWrapper

from matches.game import Game as MatchesGame
from ttt_game.ttt import Game as TTTGame
from ttt_game.ttt import State as TTTState
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
    user_session = sessions.get(user_id, Session(user_id, handlers['default']))

    while True:
        handler_result = user_session.handler(text, user_session, bot_wrapper)
        if not handler_result:
            break

    sessions[user_id] = user_session


def handle_ttt_game(text, user_session: Session, bot_wrapper):
    state = user_session.data.get('state', TTTState.not_started)

    if state == TTTState.not_started:
        user_session.data['game'] = TTTGame()
        buttons = rkm([["Easy"], ["Medium"], ["Hard"]])
        bot_wrapper.send("Select difficulty level:", buttons)
        user_session.data['state'] = TTTState.difficulty_choosing
        return False

    elif state == TTTState.difficulty_choosing:
        levels = ['easy', 'medium', 'hard']
        result, similarity = SearchEngine(levels).find(text)
        if similarity < 0.5:
            buttons = rkm([["Easy"], ["Medium"], ["Hard"]])
            message_text = "I can't recognize difficulty level, try again :)"
            bot_wrapper.send(message_text, buttons)
        else:
            message_text = "You have chosen '{}', great choice!\n Would you like to play first?".format(result)
            user_session.data['game'].set_difficulty(result)
            buttons = rkm([["Yes"], ["No"]])
            bot_wrapper.send(message_text, buttons)
            user_session.data['state'] = TTTState.player_type_choosing
        return False

    elif state == TTTState.player_type_choosing:
        answers = ['yes', 'no']
        result, similarity = SearchEngine(answers).find(text)
        if similarity < 0.5:
            buttons = rkm([["Yes"], ["No"]])
            message_text = "I can't recognize, try one more time.\n Would you like to play first?"
            bot_wrapper.send(message_text, buttons)
        else:

            if result == 'no':
                user_session.data['game'].choose_player_type(bot_wrapper, player_type='o')
            else:
                user_session.data['game'].choose_player_type(bot_wrapper, player_type='x')

            message_text = "Well, let's start!"
            buttons = rkm([["Yes"], ["No"]])
            bot_wrapper.send(message_text, buttons)
            user_session.data['state'] = TTTState.playing
        return False

    elif state == TTTState.playing:
        if len(text) == 0 and text in '123456789':
            user_session.data['game'].get_player_move(bot_wrapper, text)
        else:
            bot_wrapper.send("Wrong move format. Has to be a number from 1 to 9")
        return False
    elif state == TTTState.finished:
        user_session.data['game'] = None
        message_text = "Would you like to play one more time?"
        bot_wrapper.send(message_text)
        return False
    else:
        print("playing one more time in ttt game")
        answers = ['yes', 'no']
        result, similarity = SearchEngine(answers).find(text)
        if result == 'yes' and similarity > 0.5:
            user_session.data['state'] = TTTState.not_started
        else:
            user_session.handler = handlers['default']
        return True


def handle_big_xo_game(text, user_session, bot_wrapper):
    pass
    return True


def handle_matches_game(text, user_session, bot_wrapper):
    pass
    return True


def handle_wolfram(text, user_session, bot_wrapper):
    pass
    return True


def handle_no_activity_found(text, user_session, bot_wrapper: BotWrapper):
    text = "Sorry, I don't understand the activity you want to start. Here is the list below :)"
    bot_wrapper.send(text, main_menu)
    return False


def handle_activity_choosing(text, user_session: Session, bot_wrapper):
    global search_engine
    global handlers

    # result, similarity = search_engine.find(text)
    result, similarity = "tic-tac-toe", 0.6

    if similarity < 0.5:
        user_session.handler = handlers['no_activity_found']
        return True
    else:
        user_session.handler = handlers[result]
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
    # get from the environment
    # for simplicity it is used no
    token = '499287770:AAFLFQYCd_RqSarNy2fQAheRqCL5o2B_1ds'

    """Run bot."""
    updater = Updater(token)

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

    print("The bot is running now :)")

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

