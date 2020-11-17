def get_menu(message):
    start_menu = '/start - return to the menu'
    details_menu = '/details - return to show details'

    return "hi {} \n menu :\n{}\n{}".format(message.get_full_name(), start_menu, details_menu)


def get_wrong_msg(message):
    return "I can't understand.\nplease try again."


def get_handler(message, user_name, next_action):
    if message == '/start':
        return next_action["pre_start"]
    pre_state = '/start'#get_current_state(user_name)
    if pre_state == '/start' and message[0] != '/':
        func = get_wrong_msg
    else:
        func = next_action.get(pre_state, get_wrong_msg)
    return func
