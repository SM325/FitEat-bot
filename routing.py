from api_nutrition import get_nutritional_values


def start_handler(message):
    start_menu = '/start - return to the menu'
    details_menu = '/details - return to show details'
    update_menu = '/update - update your details'
    msg = "hi {} \n menu :\n{}\n{}\n{}".format(message.get_full_name(), start_menu, details_menu, update_menu)

    message.update_current_state("/start")
    return msg


def details_handler(message):
    msg = "please insert food..."
    message.update_current_state("/details")
    return msg


def add_handler(message):
    msg = "please insert food..."
    message.update_current_state("/add")
    return msg


def update_handler(message):
    msg = "Please enter your birth date, weight, height and gender"
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
    return "calories " + str(nutritions['calories'])


def update_the_user_details_handler(message):
    details = message.incoming_message.split()
    if len(details) != 4:
        msg = "I cant read.\n Please enter your birth date, weight, height and gender"
    else:
        # validation!!!
        birth_date = details[0]
        weight = (float)(details[1])
        height = (float)(details[2])
        gender = details[3]
        message.update_user_details(birth_date, weight, height, gender)
        msg = "update..."
        message.update_current_state("update_user_details")  # ????
    return msg


def get_wrong_msg(message):
    return "I can't understand.\nplease try again."


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
