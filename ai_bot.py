import os

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import ReplyKeyboardMarkup as rkm

from big_xo.big_xo import BigGame
from matches.matches import Matches
from translator.translator import Translator
from ttt_game.ttt import Game
from wolfram_alpha_api.wolfram import Wolfram
#from search_engine.index import SearchEngine

from config import BOT_API_TOKEN
from update2text import update2text
#from yolo_predictor import YoloPredictor

print(os.path.join(os.getcwd(), 'darknet/'))


#YOLO = YoloPredictor(os.path.join(os.getcwd(), 'darknet/'))
SEARCH_ENGINE = None
USERS = {}
MAIN_MENU = rkm([
    ['tic-tac-toe'],
    ['5 in a row'],
    ['matches'],
    ['wolfram'],
    ['translator'],
    ['detect objects']
], one_time_keyboard=True)

MAIN_MENU_AUTH = rkm([
    ['question time toggle']
])

QUEUE = [

]

isQuestionTime = False

admins = [32038583]


def start(bot, update):
    global USERS
    print("Start for user", str(update.message.from_user.id))
    USERS[update.message.from_user.id] = {}
    USERS[update.message.from_user.id]['activity'] = None
    USERS[update.message.from_user.id]['text'] = None
    if update.message.from_user.id in admins:
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text='Hi, {}!\nYour are admin here'.format(update.message.from_user.first_name),
            reply_markup=MAIN_MENU_AUTH
        )
    else:
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text='Hi, {}!\nI\'m glad to see you here.\nPlease, say sending audiomessage'
                 ' or choose below what you want to open.'.format(update.message.from_user.first_name),
            reply_markup=MAIN_MENU
        )


def show_choice(bot, update, choice):
    bot.sendMessage(
        chat_id=update.message.chat.id,
        text='Ok, {}.\nExecuting {})'.format(update.message.from_user.first_name, choice)
    )


def handle_message(bot, update):
    global SEARCH_ENGINE
    global USERS
    global isQuestionTime
    global QUEUE


    if isQuestionTime:
        if update.message.from_user.id in admins:
            isQuestionTime = not isQuestionTime
        else:
            QUEUE.append((bot, update))
        if not isQuestionTime:
            map(QUEUE, handle)
    else:
        USERS[update.message.from_user.id]['text'] = update2text(update, "en-US")

        if not USERS[update.message.from_user.id]['activity']:
            #result, similarity = SEARCH_ENGINE.find(USERS[update.message.from_user.id]['text'].lower())
            result, similarity = USERS[update.message.from_user.id]['text'], 1

            if similarity < 0.5:
                bot.sendMessage(
                    chat_id=update.message.chat.id,
                    text='I didn\'t understand you, {}!\nPlease, speak slowly and clearly. \
                    What did you want to say with this: \'{}\''.format(
                        update.message.from_user.first_name, USERS[update.message.from_user.id]['text']),
                    reply_markup=MAIN_MENU
                )

            elif result == 'tic-tac-toe':
                USERS[update.message.from_user.id]['activity'] = Game()
                show_choice(bot, update, 'tic-tac-toe')

            elif result == '5 in a row':
                USERS[update.message.from_user.id]['activity'] = BigGame(bot, update.message, 10)
                show_choice(bot, update, '5 in a row')

            elif result == 'matches':
                USERS[update.message.from_user.id]['activity'] = Matches()
                show_choice(bot, update, 'Matches')

            elif result == 'wolfram':
                USERS[update.message.from_user.id]['activity'] = Wolfram()
                show_choice(bot, update, 'WolframAlpha')

            elif result == 'translator':
                USERS[update.message.from_user.id]['activity'] = Translator()
                show_choice(bot, update, 'translator')

            elif result == 'detect objects':
                USERS[update.message.from_user.id]['activity'] = YOLO
                USERS[update.message.from_user.id]['text'] = 'detect object'
                show_choice(bot, update, 'Object detection')

            USERS[update.message.from_user.id]['activity'].first_query(bot, update)

        elif USERS[update.message.from_user.id]['text'] == 'Exit':
            USERS[update.message.from_user.id]['activity'] = None
            start(bot, update)

        else:
            USERS[update.message.from_user.id]['activity'].process(USERS[update.message.from_user.id]['text'], bot, update)


# ------------------------ Init stuff --------------------

def init_search_engine():
    global SEARCH_ENGINE
    facts = [['tic-tac-toe', 'tictactoe', 'tic tac toe'],
             ['5 in a row', '5-in-a-row', '5 in row'],
             ['matches', '21'],
             ['wolfram', 'search for', 'find', 'math', 'science'],
             ['translator', 'translate'],
             ['detect objects', 'images', 'img', 'detect']
            ]
    #SEARCH_ENGINE = SearchEngine(facts)


# --------------------------------------------------


def main():
    """Run bot."""
    updater = Updater(BOT_API_TOKEN)

    # loads model to create embeddings
    #SearchEngine.load_model()
    # initialisation of search engine
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
