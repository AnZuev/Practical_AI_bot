import requests
from bs4 import BeautifulSoup
import urllib

from Activity import Activity



class Wolfram(Activity):
    def __init__(self):
        self.APPID = "3ULTAE-HA496WGW72"
        self.API = "http://api.wolframalpha.com/v2/query?input={}&appid={}"

    def process(self, query, bot, update):
        self.ask(query)

    def ask(self, query):
        resp = requests.get(self.API.format(urllib.parse.quote_plus(query), self.APPID))
        if resp.status_code != 200:
            return None
        dom = BeautifulSoup(resp.text, "lxml")
        result = dom.queryresult.findAll("pod", id="Solution")
        if not result:
            result = dom.queryresult.findAll("pod", id="Result")
        if not result:
            result = dom.queryresult.findAll("pod", id="ChemicalNamesFormulas:ChemicalData")

        return result[0].findAll("subpod")
