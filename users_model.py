import pymysql
import datetime
from config import DB_HOST, DB_USER, DB_PASSWORD

connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    db="healthy_app",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def do_query(query_str):
    with connection.cursor() as cursor:
        cursor.execute(query_str)
        result = cursor.fetchall()
        return result

    

def do_query_with_change(query_str):
    with connection.cursor() as cursor:
        cursor.execute(query_str)
        connection.commit()
        return True


def add_user_without_init(user_name_):
    default_state = "/start"
    query = "INSERT INTO user VALUES('{}', '', 0, '1001-01-01', 0, 0, 0, 0, 0, 0, '{}')".format(user_name_, default_state)
    succ = do_query_with_change(query) 
    if succ:
        return True
    return False

def update_user_str_field(user_name, field_name, field_value):
    query= '''UPDATE user
            SET {} = '{}'
            where user_name = '{}' '''.format(field_name, field_value, user_name)
    succ = do_query_with_change(query) 
    if succ:
        return True
    return False

def update_user_non_str_field(user_name, field_name, field_value):
    query= '''UPDATE user
            SET {} = {}
            where user_name = '{}' '''.format(field_name, field_value, user_name)
    succ = do_query_with_change(query) 
    if succ:
        return True
    return False

def init_user(user_name_, name_, birth_date_, weight_, height_, max_calories_, max_fat_, max_crab_, max_protein_):
    name_res = update_user_str_field(user_name_, 'name', name_)
    is_init_res = update_user_non_str_field(user_name_, 'is_init', 1)
    birth_date_res = update_user_str_field(user_name_, 'birth_date', birth_date_)
    weight_res = update_user_non_str_field(user_name_, 'weight', weight_)
    height_res = update_user_non_str_field(user_name_, 'height', height_)
    max_calories_res = update_user_non_str_field(user_name_, 'max_calories', max_calories_)
    max_fat_res = update_user_non_str_field(user_name_, 'max_fat', max_fat_)
    max_crab_res = update_user_non_str_field(user_name_, 'max_carb', max_crab_)
    max_protein_res = update_user_non_str_field(user_name_, 'max_protein', max_protein_)

    if name_res and is_init_res and birth_date_res and weight_res and height_res and max_calories_res and max_fat_res and max_protein_res and max_crab_res:
        return True
    return False

def is_exist_user_without_init(user_name):
    res = False
    query = "SELECT * FROM user as u where u.user_name = '{}'".format(user_name)
    items = do_query(query)
    if items:
        res = True
    return res

def is_init_user(user_name):
    res = False
    query = "SELECT * FROM user as u where u.user_name = '{}' and is_init = 1".format(user_name)
    items = do_query(query)
    if items:
        res = True
    return res

def get_user(user_name):
    res = None
    query = "SELECT * FROM user as u where u.user_name = '{}'".format(user_name)
    items = do_query(query)
    if items:
        res = items[0]
    return res

def is_exist_user_day(user_name, req_date):
    res = False
    date_for_query = req_date.strftime("%Y-%m-%d")
    query = '''SELECT * 
    FROM user as u join user_day as ud 
    on u.user_name = ud.user_name
    where u.user_name = '{}' and ud.date_of_day = '{}' '''.format(user_name, date_for_query)
    items = do_query(query)
    if items:
        res = True
    return res

def add_user_day(user_name, req_date):
    date_for_query = req_date.strftime("%Y-%m-%d")
    query = "INSERT INTO user_day VALUES('{}', '{}', 0, 0, 0, 0)".format(user_name, date_for_query)
    succ = do_query_with_change(query) 
    if succ:
        return True
    return False

def get_user_day(user_name, req_date):
    res = None
    query = "SELECT * FROM user_day as ud where ud.user_name = '{}' and ud.date_of_day = '{}'".format(user_name, req_date)
    items = do_query(query)
    if items:
        res = items[0]
    return res