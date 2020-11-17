from flask import Flask, Response, request
from config import TOKEN
import requests

from bot import get_bot

app = Flask(__name__)


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    req = request.get_json()

    # res = "OK"
    # chat_id = req['message']['chat']['id']
    # res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
    #                    .format(TOKEN, chat_id, res))

    res = bot.action(req)
    if res:
        res = bot.send_message()
        return Response("success")
    else:
        return Response("fail")


if __name__ == '__main__':
    bot = get_bot()
    app.run(port=5002)
