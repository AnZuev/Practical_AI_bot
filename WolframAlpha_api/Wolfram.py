import requests
from bs4 import BeautifulSoup
import urllib
from telegram import ReplyKeyboardMarkup as rkm

from Activity import Activity
from config import APPID


class Wolfram(Activity):
    def __init__(self):
        self.API = "http://api.wolframalpha.com/v2/query?input={}&appid={}"
        self.exit = rkm([['Exit']])

    def first_query(self, bot, update):
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text="Ask your question",
            reply_markup=None
        )

    def process(self, query, bot, update):
        bot.sendChatAction(
            chat_id=update.message.chat.id,
            action='typing'
        )
        self.ask(query, bot, update)

    def ask(self, query, bot, update):
        resp = requests.get(self.API.format(urllib.parse.quote_plus(query), APPID))
        if resp.status_code != 200:
            return None
        dom = BeautifulSoup(resp.text, "lxml")
        result = dom.queryresult.findAll("pod", id="Solution")
        if not result:
            result = dom.queryresult.findAll("pod", id="Result")
        if not result:
            result = dom.queryresult.findAll("pod", id="ChemicalNamesFormulas:ChemicalData")

        subpods = result[0].findAll("subpod")
        for pod in subpods:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text=pod.plaintext.string
            )

        bot.sendMessage(
            chat_id=update.message.chat.id,
            text='You can enter and ask something else or exit',
            reply_markup=self.exit
        )
