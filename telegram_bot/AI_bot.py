from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup as rkm
from AI_bot_search import ask

main_menu = rkm([['Search'], ['Matches'], ['Tic tac toe'], ['XO 5 in a row']], one_time_keyboard=True)
show_menu = rkm([['Choose another activity']])


def start(bot, update):
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
    elif mes == 'Search':
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text='Nice!\nI can send a query to WolframAlpha search system for you.\nEnter some query below'
        )
    elif mes == 'Matches':
        handle_matches
    elif mes == 'Tic tac toe':
        handle_tic_tac_toe
    elif mes == 'XO 5 in a row':
        handle_XO5
    else:
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text='I can suggest you only 4 activities, so please, choose smth among them.',
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


def handle_matches():
    pass


def handle_tic_tac_toe():
    pass


def handle_XO5():
    pass



class Menu_filter(filters.BaseFilter):
    def filter(self, message):
        if message.text == 'Search' or message.text == 'Matches' or message.text == 'Tic tac toe' or message.text == 'XO 5 in a row' or message.text == 'Choose another activity':
            return True
        else:
            return False


def main():
    """Run bot."""
    updater = Updater("496585400:AAHBJEfVNDTcu-pIVne_xuBUf8OW_womLwg")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    menu_filter_instance = Menu_filter()
    dp.add_handler(MessageHandler(menu_filter_instance, handle_choice))
    dp.add_handler(MessageHandler(filters.Filters.text, handle_search))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
