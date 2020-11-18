import requests
from message import Message
from webhook_setup import TELEGRAM_SEND_WEBHOOK_URL, TELEGRAM_INIT_WEBHOOK_URL
import routing


class Bot:
    def __init__(self):
        self.outgoing_message = None
        self.message = None
        self.next_action = {}

    def send_message(self):
        res = requests.get(
            TELEGRAM_SEND_WEBHOOK_URL + "chat_id={}&text={}".format(self.message.chat_id, self.outgoing_message))
        return res.status_code == 200

    def action(self, req):
        '''return True if the action sucsess else -False'''

        if req.get("message"):  # edited_ message ???
            msg = req.get("message")
            self.message = Message(msg)

            handler = routing.get_handler(self.message, self.message.user_id,
                                          self.next_action)  # get_menu  # self.handlers(action)

            self.outgoing_message = handler(self.message)
            # self.message.update_current_state()
            return True
        else:
            return False

    @staticmethod
    def init_webhook(url):
        requests.get(url)

    # def add_handler(self, action, handler):
    #     self.handlers[action] = handler

    def add_next_action(self, action, func):
        self.next_action[action] = func


def get_bot():
    bot = Bot()
    bot.add_next_action("pre_start", routing.start_handler)
    bot.add_next_action("/start", {"/ask": routing.details_handler, "/add" : routing.add_handler, "/update": routing.update_handler,
    "/daily_state": routing.daily_state_handler, "/getbmi": routing.getBMI_handler})
    bot.add_next_action("/ask", routing.get_nutrition_from_details_handler)
    bot.add_next_action("/update", routing.update_the_user_details_handler)
    bot.add_next_action("/update_weight_height", routing.update_the_user_weight_height_handler)
    bot.add_next_action("/add", routing.add_nutrition_to_database_handler)
    Bot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)
    return bot
