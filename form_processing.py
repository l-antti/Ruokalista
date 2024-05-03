from flask import session

def validate_input(input_string, input, min_length, max_length, capitalize=True):
    errors = []
    if not input_string:
        errors.append(f"{input} kenttä ei voi olla tyhjä!")
    if len(input_string) < min_length:
        errors.append(f"Hieman liian lyhyt {input} kenttä! Anna vähintään {min_length} merkkiä.")
    if len(input_string) > max_length:
        errors.append(f"Nyt meni {input} kenttä pitkäksi! Maksimipituus on {max_length} merkkiä.")
    
    if capitalize and input_string:
        input_string = input_string[0].upper() + input_string[1:].lower()
    
    return input_string, errors

def process_form_data(form):
    errors = []
    fields = {
        "recipename": (3, 70),
        "instructions": (5, 500)
    }
    form_data = {}
    for field, (min_len, max_len) in fields.items():
        input_string, field_errors = validate_input(form.get(field), field, min_len, max_len)
        errors.extend(field_errors)
        form_data[field] = input_string
    
    if errors:
        raise ValueError(" | ".join(errors))
    
    # Handle ingredient information
    ingredients = []
    i = 0
    while True:
        ingredient_name = form.get(f'ingredients[{i}].name')
        ingredient_amount = form.get(f'ingredients[{i}].amount')
        ingredient_unit = form.get(f'ingredients[{i}].unit')
        if not ingredient_name:
            break
        ingredient_name, name_errors = validate_input(ingredient_name, "raaka-aine", 3, 50)
        amount, amount_errors = validate_input(ingredient_amount, "määrä", 1, 10)
        unit, unit_errors = validate_input(ingredient_unit, "yksikkö", 1, 20, capitalize=False)
        errors.extend(name_errors + amount_errors + unit_errors)
        ingredients.append({"name": ingredient_name, "amount": amount, "unit": unit})
        i += 1
    
    if errors:
        raise ValueError(" | ".join(errors))
    
    return form_data["recipename"], ingredients, form_data["instructions"]

    





