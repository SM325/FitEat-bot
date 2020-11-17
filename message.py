import users_model


class Message:

    def __init__(self, data):
        # self.outgoing_message = None
        self.incoming_message = data['text'].lower()
        self.chat_id = data['chat']['id']
        self.user_id = data['from']['id']
        self.first_name = data['from']['first_name']
        self.last_name = data['from']['last_name']
        self.date = data['date']
        if not self.__is_exist_user():
            self.__store_user()

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def __is_exist_user(self):
        return users_model.is_exist_user_without_init(self.user_id)

    def __store_user(self):
        users_model.add_user_without_init(self.user_id, self.get_full_name())

    def get_pre_state(self):
        pre_state = users_model.get_user(self.user_id).get("current_state")
        return pre_state

    def update_current_state(self, cur_state):
        users_model.update_user_state(self.user_id, cur_state)
