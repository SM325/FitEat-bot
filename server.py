from flask import Flask, Response, request
from config import TOKEN
import requests

app = Flask(__name__)

@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    req = request.get_json()
    # res = bot(req)
    res = "OK"
    chat_id = req['message']['chat']['id']
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, res))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)