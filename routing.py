def get_menu(message):
    start_menu = '/start - return to the menu'
    details_menu = '/details - return to show details'
    msg = "hi {} \n menu :\n{}\n{}".format(message.get_full_name(), start_menu, details_menu)

    message.update_current_state("/start")
    return msg


def get_details(message):
    msg = "please insert food..."
    message.update_current_state("/details")
    return msg


def get_food(message):
    msg = "details..."
    message.update_current_state("pre_start") # ????
    return msg


def get_wrong_msg(message):
    return "I can't understand.\nplease try again."


def get_handler(message, user_name, next_action):
    if message == '/start':
        return next_action["pre_start"]
    pre_state = message.pre_state
    if not pre_state:
        return get_wrong_msg
    if pre_state == '/start':
        func = next_action.get('/start').get(message.incoming_message,get_wrong_msg)
    else:
        func = next_action.get(pre_state, get_wrong_msg)
    return func
