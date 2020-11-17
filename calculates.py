import datetime


def age_by_birthday(bday):
    return datetime.datetime.now().year - bday.year


def calculate_calories(height, weight, age, gender):
    val = 0
    if gender == "male":
        val = 66.5 + (13.75 * weight) + (5.003 * height) - (6.775 * age)
    else:
        val = 655 + (9.563 * weight) + (1.85 * height) - (4.676 * age)
    return int(1.2 * val)



x = calculate_calories(1.74, 72.4, 45, "female")


def get_calories(birth_date, weight, height, gender):
    return 100

def get_carbs(birth_date, weight, height, gender):
    return 100

def get_protein(birth_date, weight, height, gender):
    return 100

def get_fats(birth_date, weight, height, gender):
    return 100
