from flask import Flask, Response, request
from bot import get_bot

app = Flask(__name__)


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    req = request.get_json()
    res = bot.action(req)
    if res:
        res = bot.send_message()
        return Response("success")
    else:
        return Response("fail")


if __name__ == '__main__':
    bot = get_bot()
    app.run(port=5002)
