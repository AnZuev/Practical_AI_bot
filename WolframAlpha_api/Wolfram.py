import requests
from bs4 import BeautifulSoup
import urllib

APP_NAME = "Easy Solver"
APPID = "3ULTAE-HA496WGW72"
API = "http://api.wolframalpha.com/v2/query?input={}&appid={}"


def ask(query):
    resp = requests.get(API.format(urllib.parse.quote_plus(query), APPID))
    if resp.status_code != 200:
        return None
    dom = BeautifulSoup(resp.text, "lxml")
    result = dom.queryresult.findAll("pod", id="Solution")
    if not result:
        result = dom.queryresult.findAll("pod", id="Result")
    if not result:
        result = dom.queryresult.findAll("pod", id="ChemicalNamesFormulas:ChemicalData")

    return result[0].findAll("subpod")
