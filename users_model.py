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

def add_user(user_name_, name_, birth_date_, weight_, height_, max_calories_, max_fat_, max_crab_, max_protein_, current_state_ = "main"):
    date_for_query = birth_date_.strftime("%Y-%m-%d")
    query = "INSERT INTO user VALUES('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, '{}')".format(user_name_, name_, date_for_query, weight_, height_, max_calories_, max_fat_, max_crab_, max_protein_, current_state_)
    succ = do_query_with_change(query) 
    if succ:
        return True
    return False

def is_exist_user(user_name):
    res = False
    query = "SELECT * FROM user as u where u.user_name = '{}'".format(user_name)
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
