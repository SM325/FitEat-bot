import requests

from message import Message
from webhook_setup import TELEGRAM_SEND_WEBHOOK_URL, TELEGRAM_INIT_WEBHOOK_URL

import routing


def get_menu(message):
    return "menu"


class Bot:
    def __init__(self):
        self.outgoing_message = None
        self.message = None
        # self.handlers = {}
        self.next_func = {}

    def send_message(self):
        res = requests.get(
            TELEGRAM_SEND_WEBHOOK_URL + "chat_id={}&text={}".format(self.message.chat_id, self.outgoing_message))
        return res.status_code == 200

    def action(self, req):
        '''return True if the action sucsess else -False'''

        if req.get("message"):  # edited_ message ???
            msg = req.get("message")
            self.message = Message(msg)

            action = "/start"  # self.message["text"]
            handler = routing.get_handler(self.message.incoming_message, self.message.user_id, self.next_func)  # get_menu  # self.handlers(action)

            self.outgoing_message = handler(self.message)
            # update the pre state in DB to this
            return True
        else:
            return False

    @staticmethod
    def init_webhook(url):
        requests.get(url)

    # def add_handler(self, action, handler):
    #     self.handlers[action] = handler

    def add_next_func(self, action, func):
        self.next_func[action] = func


def get_bot():
    bot = Bot()
    bot.add_next_func("pre_start", get_menu)
    # bot.add_handler("/start", get_menu)
    Bot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)
    return bot
