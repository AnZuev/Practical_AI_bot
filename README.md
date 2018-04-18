# Overview
This repository contains source code for Telegram-bot (see https://t.me/helping_to_have_fun_bot or @helping_to_have_fun_bot)
</br>
This is a quite simple bot that can:
- Play tic-tac-toe
- Play 5 in a row game
- Play Matches
- Translate Ru -> En and En -> Ru
- Solve math problems like equations, compute something, take derivatives and integrals
- Detect objects from the picture

Bot also understands natural language (for now only English) and can be controlled by voice as well.

# If you want to have your own zoo:
1. Cloning the repo
```bash
git clone https://github.com/AnZuev/Practical_AI_bot.git
```
2. Installing all the requirements
```bash
cd Practical_AI_bot;
python setup.py install
```
3. Installing darknet to the repo (see https://pjreddie.com/darknet/install/ for details)
```bash
git clone https://github.com/pjreddie/darknet.git
cd darknet
make
```
4. Download pre-trained model yolov3.weights
```bash
wget https://pjreddie.com/media/files/yolov3.weights
```
5. Download pre-trained model wiki_unigrams.bin from https://drive.google.com/file/d/0B6VhzidiLvjSa19uYWlLUEkzX3c/view and put them to the root of the project
6. Create file config.py at the root of the project and fill it with the content below and save
```bash
BOT_API_TOKEN = "YOUR_TOKEN_VALUE"
YANDEX_API_KEY = "YOUR_YANDEX_API_KEY"
YANDEX_TRANS_KEY = "YOUR_YANDEX_TRANSLATE_KEY"
APPID = "YOUR WOLFRAM_APP_ID"
```
7. Create directory *imgs* for storing images at the root of the project
```bash
mkdir imgs
```
8. Start this amazing bot!
```bash
python3 ai_bot.py
```


# Stack of technologies
- python_telegram_bot for bot development
- sklearn and sent2vec for natural language understanding
- darknet for object recognition
- numpy for 5 in a row game
- yandex-translate for translating
- Wolfram and Yandex API to solve math problems and transform speech to text correspondingly
