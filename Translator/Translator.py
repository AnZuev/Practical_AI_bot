from Activity import Activity

# pip install yandex-translater

class Translator(Activity):
import locale
from yandex import Translater
from .. import update2text.update2text

locale.setlocale(locale.LC_ALL, '')
YANDEX_API_KEY="877f02a7-6e01-494e-bb36-b999b189f036"


    def __init__(self):
		self.translator = Translater()
		self.translator.set_key(YANDEX_API_KEY)
		self.mode='EN-->RU'

    def first_query(self, bot, update):
		self.__init__()
        self.mode = rkm([['EN-->RU'], ['RU-->EN']])
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text="Select languages:",
            reply_markup=choice
        )

    def process(self, query, bot, update):
		result=""
		
        if query=='RU-->EN':
			self.translator.set_from_lang('ru')
			self.translator.set_to_lang('en')
			ans=update2text(update, BOT_API_TOKEN, "ru-RU")
			if ans!=None:
				self.translator.set_text(ans)
				result=self.translator.translate()
			
		elif query=='EN-->RU':
			self.translator.set_from_lang('en')
			self.translator.set_to_lang('ru')
			ans=update2text(update, BOT_API_TOKEN, "en-US")
			if ans!=None:
				self.translator.set_text(ans)
				result=self.translator.translate()
				
		if len(result)==0:
			result="What? try again, keep calm speak slowly and clearly."
			
		return result