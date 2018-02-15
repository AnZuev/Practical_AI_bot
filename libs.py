# ------------------------ etc --------------------


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


class Session:
    def __init__(self, user_id, def_handler):
        self.data = dict()
        self.user_id = user_id
        self.handler = def_handler

# --------------------------------------------------
