from config import APP_ID_NUTRITIONIX, APP_KEY_NUTRITIONIX
import requests
import calculations

def get_products_list(product):
    params_to_send = {
        "appId": APP_ID_NUTRITIONIX,
        "appKey": APP_KEY_NUTRITIONIX,
        "fields": ["item_name", "item_type", "nf_calories", "nf_total_fat", "nf_total_carbohydrate", "nf_protein",
                   "nf_serving_weight_grams"],
        "query": product,
        "filters": {
            "item_type": 2,
            "nf_serving_weight_grams": {
                "from": 0
            }
        }
    }
    result = requests.post(" https://api.nutritionix.com/v1_1/search", json=params_to_send)
    return result.json().get('hits')

def get_item(products, product_name_words):
    if not products:
        return None
    for item in products:
        item_name_words = set(item.get('fields').get('item_name').lower().split(" "))
        if product_name_words.issubset(item_name_words) and len(product_name_words) == len(item_name_words):
            return item

    for item in products:
        item_name_words = set(item.get('fields').get('item_name').lower().split(" "))
        if product_name_words.issubset(item_name_words) and len(product_name_words) > 1:
            return item


def get_nutritional_values(product, weight):
    products = get_products_list(product)
    product_name_words = set(product.lower().split(" "))
    item = get_item(products, product_name_words)
    if item:
        fields = item.get('fields')
        print(fields)
        item_dict = calculations.get_nutritions_by_weight(fields, weight)
        return item_dict

if __name__ == '__main__':
    print(get_nutritional_values("chocolate", 30))
    # print(get_nutrition_from_details_handler("chocolate 30"))
    # print(get_nutrition_from_details_handler("chocolate"))
    # print(get_nutrition_from_details_handler("100"))
    # print(get_nutrition_from_details_handler("home fries 100"))
    # print(get_nutrition_from_details_handler("homde fries 100"))