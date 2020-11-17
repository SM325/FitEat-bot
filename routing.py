from api_nutrition import get_nutritional_values
import users_model
import calculations

def start_handler(message):
    start_menu = '/start - return to the menu'
    details_menu = '/details - return to show details'
    update_menu = '/update - update your details'
    msg = "hi {} \n menu :\n{}\n{}\n{}".format(message.get_full_name(), start_menu, details_menu, update_menu)

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

def add_nutrition_to_database(message):
    nutritions = get_nutritions(message)
    if not nutritions:
        return get_wrong_msg(message)
    users_model.update_nutrition(message.user_id, message.date, nutritions['calories'], nutritions['fat'], nutritions['carb'], nutritions['protein'])


def get_nutrition_from_details_handler(message):
    nutritions = get_nutritions(message)
    if not nutritions:
        return get_wrong_msg(message)
    return display_nutritions_list(nutritions)

def get_nutritions(message):
    message_word = message.incoming_message.split(" ")
    if message_word[0].isdigit():
        return None
    if not message_word[-1].isdigit():
        weight = 100
        product = message.incoming_message
    else:
        weight = int(message_word[-1])
        product = " ".join(message_word[:-1])
    return get_nutritional_values(product, weight)

def display_nutritions_list(nutritions):
    nutritions_list = "Displays nutritional values for: {}, {}g".format(nutritions['item_name'], nutritions['weight'])
    nutritions_list += "\n\nCalories: " + str(nutritions['calories'])
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

def getBMI_handler(message):
    user = users_model.get_user(message.user_id)
    if user.get('is_init') == 1:
        bmi = calculations.calculate_bmi(user['weight'], user['height'])
        normal_weight = calculations.calculate_normal_weight(user['weight'])
        bmi_print = "your BMI is: " + str(bmi)
        normal_weight_print = "\nNormal weight for your height is:\n" + str(normal_weight[0]) + " to " + str(normal_weight[1])
        bmi_category = calculations.get_bmi_category(bmi)
        return bmi_print + "\n" + bmi_category + "\n" + normal_weight_print
    else:
        msg = "You have to update your details, please enter /update to update"
        message.update_current_state("/start")
        return msg