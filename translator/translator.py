import locale
from yandex import Translater
from update2text import update2text
from telegram import ReplyKeyboardMarkup as rkm

from activity import Activity
from config import BOT_API_TOKEN
from config import YANDEX_API_KEY


class Translator(Activity):
    def __init__(self):

        locale.setlocale(locale.LC_ALL, '')
        self.translator = Translater()
        self.translator.set_key(YANDEX_API_KEY)
        self.mode = 'EN-->RU'
        self.default_markup = rkm([['Exit']])

    def first_query(self, bot, update):
        self.__init__()
        self.mode = rkm([['EN-->RU'], ['RU-->EN']], one_time_keyboard=True)
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text="Select languages:",
            reply_markup=self.mode
        )

    def process(self, query, bot, update):

        result = ""

        if query == 'RU-->EN':
            self.translator.set_from_lang('ru')
            self.translator.set_to_lang('en')
            self.locale = "ru-RU"
        elif query == 'EN-->RU':
            self.translator.set_from_lang('en')
            self.translator.set_to_lang('ru')
            self.locale = "en-US"
        else:
            ans = update2text(update, self.locale)
            if ans != None:
                self.translator.set_text(ans)
                result = self.translator.translate()

            bot.sendMessage(
                chat_id=update.message.chat.id,
                text=result,
                reply_markup=self.default_markup
            )

        if len(result) == 0:
            result = "What? try again, keep calm speak slowly and clearly."
