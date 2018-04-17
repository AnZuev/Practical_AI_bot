import requests
import uuid
from bs4 import BeautifulSoup
from config import YANDEX_TRANS_KEY



def update2text(update, locale):  # locale="ru-RU" or "en-US"
    message = update.message

    text = ""

    if message.text is not None:
        text = message.text  # если в сообщении есть текст, то берём его для начала

    if message.voice != None:  # если есть голос, то попробуем его распознать
        file_info = message.bot.get_file(message.voice.file_id)

        file = requests.get(file_info.file_path)  # вроде точно так из телеги файлы выкачиваются

        UUID = str(uuid.uuid4()).replace("-", "")
        answer = speech_2_text(file.content, UUID, locale)  # пробуем распознать

        if len(answer) != 0:
            mv = max(answer, key=answer.get)  # если удалось распознать речь, то берём лучшее совпадение
            text = mv

    if len(text) == 0:
        text = None  # если в сообщении нет текста или не удалось распознать текст.
    return text


def speech_2_text(data, uid, lang):
    url = "https://asr.yandex.net/asr_xml?uuid={}&key={}&topic={}&lang={}&disableAntimat={}"
    url = url.format(uid, YANDEX_TRANS_KEY, "queries", lang, "true")

    headers = {'Content-Type': 'audio/ogg;codecs=opus', 'Content-Length': str(len(data))}

    resp = requests.post(url, data=data, headers=headers)

    dom = BeautifulSoup(resp.text, "lxml")
    result = dict((var.string, float(var['confidence']))
                  for var
                  in dom.html.body.recognitionresults.findAll("variant"))

    return result
