import datetime


def age_by_birthday(bday):
    return datetime.datetime.now().year - bday.year


def get_calories(birth_date, weight, height, gender):
    age = age_by_birthday(birth_date)
    if gender == "male":
        val = 66.5 + (13.75 * weight) + (5.003 * height) - (6.775 * age)
    else:
        val = 655 + (9.563 * weight) + (1.85 * height) - (4.676 * age)
    return int(1.2 * val)


def get_carbs(birth_date, weight, height, gender):
    return int(get_calories(birth_date, weight, height, gender) * 0.5)


def get_protein(birth_date, weight, height, gender):
    return int(get_calories(birth_date, weight, height, gender) * 0.3)


def get_fats(birth_date, weight, height, gender):
    return int(get_calories(birth_date, weight, height, gender) * 0.2)

ca = get_calories(datetime.datetime(1998, 3, 1), 70, 1.70, "female")
car = get_carbs(datetime.datetime(1998, 3, 1), 70, 1.70, "female")
p = get_protein(datetime.datetime(1998, 3, 1), 70, 1.70, "female")
f = get_fats(datetime.datetime(1998, 3, 1), 70, 1.70, "female")


print(ca, car, p, f)