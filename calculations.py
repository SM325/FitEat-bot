from decimal import Decimal

def get_nutritions_by_weight(fields, weight_user):
    weight_item = fields.get('nf_serving_weight_grams')
    new_value = lambda v: round((v/weight_item) * weight_user, 2)
    item_dict = {
        'item_name': fields.get('item_name'),
        'calories': new_value(fields.get('nf_calories')),
        'fat': new_value(fields.get('nf_total_fat')),
        'carb': new_value(fields.get('nf_total_carbohydrate')),
        'protein': new_value(fields.get('nf_protein'))
    }
    return item_dict