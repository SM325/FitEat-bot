import users_model
import calculations
import datetime


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
        if self.is_exist_init_user():
            if not self.is_exist_user_day(datetime.datetime.now()):
                self.add_user_day(datetime.datetime.now())

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

    def update_user_details(self, birth_date, weight, height, gender):
        calories = calculations.get_calories(birth_date, weight, height, gender)
        fats = calculations.get_fats(birth_date, weight, height, gender)
        crabs = calculations.get_carbs(birth_date, weight, height, gender)
        protein = calculations.get_protein(birth_date, weight, height, gender)
        users_model.init_user(self.user_id, self.get_full_name(), birth_date, weight, height, calories, fats, crabs,
                              protein, gender)
    
    def is_exist_init_user(self):
        return users_model.is_init_user(self.user_id)

    def get_user_day(self, date):
        return users_model.get_user_day(self.user_id, date)

    def get_user(self):
        return users_model.get_user(self.user_id)

    def add_user_day(self, date):
        return users_model.add_user_day(self.user_id, date)

    def is_exist_user_day(self, date):
        return users_model.is_exist_user_day(self.user_id, date)
