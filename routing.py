from api_nutrition import get_nutritional_values
import datetime


def start_handler(message):
    start_menu = '/start - return to the menu'
    details_menu = '/details - return to show details'
    update_menu = '/update - update your details'
    daily_state_menu = '/daily_state - display your daily state'
    msg = "Hi {} \n menu :\n{}\n{}\n{}\n{}".format(message.get_full_name(), start_menu, details_menu, update_menu, daily_state_menu)

    message.update_current_state("/start")
    return msg


def details_handler(message):
    msg = "please insert food and amount(g.)"
    message.update_current_state("/details")
    return msg


def add_handler(message):
    msg = "please insert food and amount(g.)"
    message.update_current_state("/add")
    return msg


def update_handler(message):
    msg = "Please enter your birth date (YYYY-MM-DD), weight(kg), height(meter) and gender(male/female)"
    message.update_current_state("/update")
    return msg

def daily_state_handler(message):
    cur_date = datetime.datetime.now()
    if not message.is_exist_init_user():
        message.update_current_state("/start")
        # go to start hendler
        return "Your details is already init.\n Please go to update before from /start"
    
    daily_details = message.get_user_day(cur_date)
    user_details = message.get_user()

    carb_dif = user_details.get("max_carb") - daily_details.get("carb")
    calories_dif = user_details.get("max_calories") - daily_details.get("calories")
    fat_dif = user_details.get("max_fat") - daily_details.get("fat")
    protein_dif = user_details.get("max_protein") - daily_details.get("protein")

    msg = "carb dif "+ (str)(carb_dif)
    msg += "calories_dif "+ (str)(calories_dif)
    msg += "fat_dif "+ (str)(fat_dif)
    msg += "protein_dif dif "+ (str)(protein_dif)

    message.update_current_state("/update")
    return msg


def get_nutrition_from_details_handler(message):
    message_word = message.incoming_message.split(" ")
    if message_word[0].isdigit():
        return get_wrong_msg(message)
    if not message_word[-1].isdigit():
        weight = 100
        product = message.incoming_message
    else:
        weight = int(message_word[-1])
        product = " ".join(message_word[:-1])
    nutritions = get_nutritional_values(product, weight)
    if not nutritions:
        return get_wrong_msg(message)
    return display_nutritions_list(nutritions, weight)

def display_nutritions_list(nutritions, weight):
    nutritions_list = "Displays nutritional values for {}, {}g".format(nutritions['item_name'], str(weight))
    nutritions_list += "\nCalories: " + str(nutritions['calories'])
    nutritions_list += "\nfat: " + str(nutritions['fat'])
    nutritions_list += "\ncarb: " + str(nutritions['carb'])
    nutritions_list += "\nprotein: " + str(nutritions['protein'])
    return nutritions_list




def update_the_user_details_handler(message):
    details = message.incoming_message.split()
    if len(details) != 4:
        msg = "I cant read.\n Please enter your birth date (YYYY-MM-DD), weight(k.g.), height(m.) and gender(male/female)"
    else:
        # validation!!!
        birth_date = details[0]
        weight = (float)(details[1])
        height = (float)(details[2])
        gender = details[3]
        message.update_user_details(birth_date, weight, height, gender)
        msg = "good, I update your details"
        message.update_current_state("update_user_details")
    return msg


def get_wrong_msg(message):
    return "I can't understand.\nplease try again or enter /start to menu"


def get_handler(message, user_name, next_action):
    if message.incoming_message == '/start':
        return next_action["pre_start"]
    pre_state = message.get_pre_state()
    if not pre_state:
        return get_wrong_msg
    if pre_state == '/start':
        func = next_action.get('/start').get(message.incoming_message, get_wrong_msg)
    else:
        func = next_action.get(pre_state, get_wrong_msg)
    return func
