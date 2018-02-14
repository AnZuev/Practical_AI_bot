import requests
import uuid
from bs4 import BeautifulSoup


YANDEX_API_KEY="key" # put your key here


def update2text(update):
    message=update.message

    text=bot.get_file(message.text) # если в сообщении есть текст, то берём его для начала

    if message.voice!=null: # если есть голос, то попробуем его распознать
        file_info = bot.get_file(message.voice.file_id) 
        file = requests.get(
            'https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path)) # вроде так из телеги файлы выкачиваются
        
        UUID = str(uuid.uuid4()).replace("-", "")
        answer = speech_2_text(file.content, UUID) # пробуем распознать

        if len(answer)!=0:
            mv=max(answer, key=answer.get) # если удалось распознать речь, то берём лучшее совпадение
            text=mv 

    if len(text)==0:
        text="What? Moia tvoia ne ponimat. Try again!" # если в сообщении нет текста или не удалось распознать текст.
    return text


# this is unique idenifier of user
# API assumes that APPLICATION makes requests and we can mark them


def speech_2_text(data, uid, lang="ru_RU"):
    
    url = "https://asr.yandex.net/asr_xml?uuid={}&key={}&topic={}&lang={}&disableAntimat={}"
    url = url.format(uid, YANDEX_API_KEY, "queries", lang, "true")
    

    headers = {'Content-Type' : 'audio/ogg;codecs=opus', 'Content-Length' : str(len(data))}

    resp = requests.post(url, data=data, headers=headers)
    
    dom = BeautifulSoup(resp.text, "lxml")    
    result = dict((var.string, float(var['confidence']))   
                  for var 
                  in dom.html.body.recognitionresults.findAll("variant"))
    
    return result