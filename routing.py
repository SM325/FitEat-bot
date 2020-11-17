def display_nutritions(bot):
    pass

def display_menue(bot):
    pass

def error_func():
    pass


next_func = {'details_func': display_nutritions,}

def get_current_state():
    pass

def find_action(message, user_name, next_func):
    if  message == '/start':
        return display_menue
    pre_state = get_current_state(user_name)
    if pre_state == '/start' and message[0] != '/':
        func = error_func
    else:
        func = next_func.get(pre_state, error_func)
    return func