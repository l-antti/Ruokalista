# form module
# käsittelee lomakkeiden dataaa

from flask import session



def validate_input(input_string, input, min_length, max_length):
    if not input_string:
        raise ValueError(f"{input}-kenttä ei voi olla tyhjä!")
    elif len(input_string) < min_length:
        raise ValueError(f"Hieman liian lyhyt {input}-kenttä! Anna vähintään {min_length} merkkiä.")
    elif len(input_string) > max_length:
        raise ValueError(f"Nyt meni {input}-kenttä pitkäksi! Maksimipituus on {max_length} merkkiä.")
    return input_string
    
    
def process_form_data(form):
    # Tarkistetaan syötteet
    name = validate_input(form.get("name"), "reseptin nimi", 3, 50)
    instructions = validate_input(form.get("instructions"),"valmistusohje", 5, 500)
    
    # Käsitellään raaka-aineiden tiedot
    ingredient_names = form.getlist("ingredientName")
    ingredient_amounts = form.getlist("ingredientAmount")
    ingredient_units = form.getlist("ingredientUnit")
    
    # Tarkistetaan jokainen raaka-aine
    ingredients = []
    for i in range(len(ingredient_names)):
        name = validate_input(ingredient_names[i], "raaka-aine", 3, 50)
        amount = validate_input(ingredient_amounts[i], "määrä", 1, 10)
        unit = validate_input(ingredient_units[i], "yksikkö", 1, 20)
        ingredients.append({"name": name, "amount": amount, "unit": unit})
    
    return name, instructions, ingredients
