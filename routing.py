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
    msg = "please enter your birth_date, weight and height..."
    message.update_current_state("/update")
    return msg

def get_nutrition_from_details_handler(message):
    msg = "details..."
    message.update_current_state("nutrition_from_details")  # ????
    return msg

def update_the_user_details_handler(message):
    
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
