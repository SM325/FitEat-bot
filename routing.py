from api_nutrition import get_nutritional_values
import users_model
import calculations
import datetime


def start_handler(message):
    description = "I will help you keep track of your daily nutrition " \
                  "and give you recommendations according to your current state.\n\n"
    start_menu = '/start - display menu\n\n'
    details_menu = '/ask - view a product nutritional values and recommendations\n\n'
    update_menu = '/update - update your details (for better results)\n\n'
    daily_state_menu = '/daily_state - view your daily state\n\n'
    add_food_menu = '/add - add a product you have eaten to your daily menu\n\n'
    get_bmi_menu = '/getBMI - view your BMI'
    msg = "Hi {} \U0001F603 welcome!!\nI am Healthy-Bot \U0001F643\n\n{}{}{}{}{}{}{}".format(message.get_full_name(),description, start_menu, details_menu, update_menu,
     daily_state_menu, add_food_menu, get_bmi_menu)


    message.update_current_state("/start")
    return msg


def details_handler(message):
    msg = "Please insert food and amount(g.)\n For example: chocolate 30"
    message.update_current_state("/ask")
    return msg


def add_handler(message):
    if message.is_exist_init_user():
        msg = "Please insert food and amount(g.)\n For example: chocolate 30"
        message.update_current_state("/add")
    else:
        msg = "I'm missing your details.\ngo to /update"
        message.update_current_state("/start")
    return msg


def update_handler(message):
    if message.is_exist_init_user():

        msg = "Please enter your weight(kg) and height(meter)\nFor example: 80 1.80"
        message.update_current_state("/update_weight_height")
    else:
        msg = "Please enter your age, weight(kg), height(meter) and gender(male/female)" \
              "\n For example: 27 80 1.80 male"
        message.update_current_state("/update")
    return msg


def add_to_match_list(value, percent, val_name, pos_details_list, neg_details_list, zero_details_list):
    if value == 0:
        zero_details_list.append("{}\n".format(val_name))
    if value > 0:
        pos_details_list.append(
            "{} {}, it is {}% of your daily amount \n".format(int(value), val_name, 100 - int(percent)))
    if value < 0:
        neg_details_list.append(
            "{} {}, it is {}% more then daily amount \n".format(-1 * int(value), val_name, int(percent) - 100))


def daily_state_handler(message):
    msg = "Your today status:\n"
    cur_date = datetime.datetime.now()
    if not message.is_exist_init_user():
        message.update_current_state("/start")
        # go to start hendler
        return "You have to update your details first, please enter /update to update"
    daily_details = message.get_user_day(cur_date)
    user_details = message.get_user()

    carb_dif = user_details.get("max_carb") - daily_details.get("carb")
    calories_dif = user_details.get("max_calories") - daily_details.get("calories")
    fat_dif = user_details.get("max_fat") - daily_details.get("fat")
    protein_dif = user_details.get("max_protein") - daily_details.get("protein")

    carb_percent = 100 * daily_details.get("carb") / user_details.get("max_carb")
    calories_percent = 100 * daily_details.get("calories") / user_details.get("max_calories")
    fat_percent = 100 * daily_details.get("fat") / user_details.get("max_fat")
    protein_percent = 100 * daily_details.get("protein") / user_details.get("max_protein")

    pos_list = list()
    nag_list = list()
    zero_list = list()

    pos_details = "You have left: \n"
    neg_details = "You have exceeded: \n"
    zero_details = "You finish: \n"

    add_to_match_list(calories_dif, calories_percent, "calories", pos_list, nag_list, zero_list)
    add_to_match_list(carb_dif, carb_percent, "carbs", pos_list, nag_list, zero_list)
    add_to_match_list(fat_dif, fat_percent, "fats", pos_list, nag_list, zero_list)
    add_to_match_list(protein_dif, protein_percent, "proteins", pos_list, nag_list, zero_list)

    if len(pos_list):
        for str_ in pos_list:
            pos_details += str_
        msg += pos_details
    if len(nag_list):
        for str_ in nag_list:
            neg_details += str_
        msg += neg_details
    if len(zero_list):
        for str_ in zero_list:
            zero_details += str_
        msg += zero_details

    message.update_current_state("/start")
    return msg


def add_nutrition_to_database_handler(message):
    nutritions = get_nutritions(message)
    if not nutritions:
        return get_wrong_msg(message)
    insertion_ok = users_model.update_nutrition(message.user_id, datetime.datetime.now(), nutritions['calories'],
                                                nutritions['fat'], nutritions['carb'], nutritions['protein'])
    if insertion_ok:
        #        message.update_current_state("/start")
        state_str = daily_state_handler(message)
        message.update_current_state("/add")
        return "OK, I added: {}g to your daily nutrition \n\n{}".format(message.incoming_message, state_str)
    return get_wrong_msg(message)


def get_nutrition_from_details_handler(message):
    nutritions = get_nutritions(message)
    if not nutritions:
        return get_wrong_msg(message)
    res = get_recommendations(message, nutritions.get("calories"))
    return display_nutritions_list(nutritions) + "\n" + res


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
    nutritions_list = "Nutritional values for: {}, {}g:".format(nutritions['item_name'], nutritions['weight'])
    nutritions_list += "\n\nCalories: " + str(nutritions['calories'])
    nutritions_list += "\nfat: " + str(nutritions['fat'])
    nutritions_list += "\ncarb: " + str(nutritions['carb'])
    nutritions_list += "\nprotein: " + str(nutritions['protein'])
    return nutritions_list



def validate_all_user_details (details):
    res = True
    try:
        tmp = float(details[0])
        tmp = float(details[1])
        tmp = float(details[2])
        if not (details[3] in ['male', 'female']):
            res = False
    except ValueError:
        res = False
    return res

def update_the_user_details_handler(message):
    details = message.incoming_message.split()
    if len(details) != 4 or not validate_all_user_details(details):
        msg = "I can't understand you \U0001F622\n Please enter your age, weight(kg), height(meter) and gender(male/female)" \
              "in this format\n For example: 27 80 1.80 male"
    else:
        age = float(details[0])
        weight = (float)(details[1])
        height = (float)(details[2])
        gender = details[3]
        if (age - int(age) >= 0.5):
            age = int(age) + 1
        else:
            age = int(age)
        birth_date = calculations.birthday_by_age(age)
        str_birth_date =  birth_date.strftime("%Y-%m-%d")
        message.update_user_details(str_birth_date, weight, height, gender)
        msg = "good, I update your details"
        message.update_current_state("/start")
    return msg

def validate_weight_height_details (details):
    res = True
    try:
        tmp = float(details[0])
        tmp = float(details[1])
    except ValueError:
        res = False
    return res

def update_the_user_weight_height_handler(message):
    details = message.incoming_message.split()
    if len(details) != 2 or not validate_weight_height_details(details):
        msg = "I can't understand you \U0001F622\n Please enter your weight(kg) and height(meter) in this format" \
              "\n For example: 80 1.80"
    else:
        user_details = message.get_user()
        birth_date = user_details.get("birth_date").strftime("%Y-%m-%d")
        weight = (float)(details[0])
        height = (float)(details[1])
        gender = user_details.get("gender")
        message.update_user_details(birth_date, weight, height, gender)
        msg = "good, I update your details"
        message.update_current_state("/start")
    return msg


def get_wrong_msg(message):
    return "Sorry, I can't understand you \U0001F622 \nPlease try again or enter /start to go " \
           "to the main menu"


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
    user = message.get_user()
    message.update_current_state("/start")
    if message.is_exist_init_user():
        bmi = calculations.calculate_bmi(user['weight'], user['height'])
        normal_weight = calculations.calculate_normal_weight(user['height'])
        bmi_print = "your BMI is: " + str(bmi)
        normal_weight_print = "\nNormal weight for your height is:\n" + str(normal_weight[0]) + " to " + str(
            normal_weight[1])
        bmi_category = calculations.get_bmi_category(bmi)
        return bmi_print + "\n" + bmi_category + "\n" + normal_weight_print
    else:
        msg = "You have to update your details first, please enter /update to update"
        return msg


def get_recommendations(message, calories):
    user = message.get_user()
    user_day = message.get_user_day(datetime.datetime.now())
    if message.is_exist_init_user():
        if user_day.get("calories") + calories <= user.get("max_calories"):
            return "\nOK. Looks like you can eat it"
        else:
            return "\nSorry, This food will make you exceed your daily calories"
    else:
        message.update_current_state("/start")
        msg = "\nI'm missing details so I can't give you recommendations.\ngo to /update"
        return msg

