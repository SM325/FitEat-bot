import datetime

def get_nutritions_by_weight(fields, weight_user):
    weight_item = fields.get('nf_serving_weight_grams')
    new_value = lambda v: round((v / weight_item) * weight_user, 2)
    item_dict = {
        'item_name': fields.get('item_name'),
        'calories': new_value(fields.get('nf_calories')),
        'fat': new_value(fields.get('nf_total_fat')),
        'carb': new_value(fields.get('nf_total_carbohydrate')),
        'protein': new_value(fields.get('nf_protein')),
        'weight': weight_user
    }
    return item_dict


def age_by_birthday(bday):
    datetime_object = datetime.datetime.strptime(bday, '%Y-%m-%d')
    print(datetime_object)
    return datetime.datetime.now().year - datetime_object.year


def get_calories(birth_date, weight, height, gender):
    age = age_by_birthday(birth_date)
    if gender == "male":
        val = 66.5 + (13.75 * weight) + (5.003 * height) - (6.775 * age)
    else:
        val = 655 + (9.563 * weight) + (1.85 * height) - (4.676 * age)
    return int(1.2 * val)


def get_carbs(birth_date, weight, height, gender):
    return int(get_calories(birth_date, weight, height, gender) * 0.5 / 4)


def get_protein(birth_date, weight, height, gender):
    return int(get_calories(birth_date, weight, height, gender) * 0.3 / 4)


def get_fats(birth_date, weight, height, gender):
    return int(get_calories(birth_date, weight, height, gender) * 0.2/ 9)


def calculate_bmi(weight, height):
    return round((weight) / (height ** 2), 2)


def calculate_normal_weight(height):
    start_weight = round((18.5 * (height ** 2)), 2)
    end_weight = round((24.9 * (height ** 2)), 2)
    return start_weight, end_weight


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Your weight is too low, you have to eat more... \U0001F968	"
    elif bmi < 24.9:
        return "Your weight is good, Well done!!! \U0001F44C"
    elif bmi < 29.9:
        return "Your weight is too high..., please try to eat healthier \U0001F609\n I'm sure you can \U0001F4AA"
    else:
        return "Unfortunately your weight is very high \nLet's start maintaining a proper diet\nI'm sure you can do this! \U0001F4AA"


def birthday_by_age(age):
    datetime_object = datetime.datetime.now()
    endDate = datetime_object.replace(year=datetime_object.year - age)
    print(endDate)
    return endDate
