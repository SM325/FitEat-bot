class Message:

    def __init__(self, data):
        self.outgoing_message = None
        self.incoming_messag = data['text'].lower()
        self.chat_id = data['chat']['id']
        self.user_id = data['from']['id']
        self.first_name = data['from']['first_name']
        self.last_name = data['from']['last_name']
        self.date = data['date']
        if not self.__is_exist_user():
            self.__store_user()

    def __is_exist_user(self):
        pass

    def __store_user(self):
        pass


