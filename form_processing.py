# form processing module

from flask import session


def validate_input(input_string, input, min_length, max_length, capitalize=True):
    if not input_string:
        raise ValueError(f"{input} kenttä ei voi olla tyhjä!")
    elif len(input_string) < min_length:
        raise ValueError(f"Hieman liian lyhyt {input} kenttä! Anna vähintään {min_length} merkkiä.")
    elif len(input_string) > max_length:
        raise ValueError(f"Nyt meni {input} kenttä pitkäksi! Maksimipituus on {max_length} merkkiä.")
        
    # Harmonize database input    
    if capitalize:
        input_string = input_string[0].upper() + input_string[1:].lower()
    
    return input_string


def process_form_data(form):
    # Check input
    recipename = validate_input(form.get("recipename"), "reseptin nimi", 3, 50)
    instructions = validate_input(form.get("instructions"),"valmistusohje", 5, 500)
    
    # Handle ingredient information
    ingredients = []
    i = 0
    while True:
        ingredient_name = form.get('ingredients[' + str(i) + '].name')
        ingredient_amount = form.get('ingredients[' + str(i) + '].amount')
        ingredient_unit = form.get('ingredients[' + str(i) + '].unit')
        if not ingredient_name:
            break
        ingredient_name = validate_input(ingredient_name, "raaka-aine", 3, 50)
        amount = validate_input(ingredient_amount, "määrä", 1, 10)
        unit = validate_input(ingredient_unit, "yksikkö", 1, 20, capitalize=False)
        ingredients.append({"name": ingredient_name, "amount": amount, "unit": unit})
        i += 1
    
    return recipename, ingredients, instructions
    





