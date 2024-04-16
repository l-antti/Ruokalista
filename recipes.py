# recipe module
# uusien reseptien lisääminen, selaus, reseptien etsiminen nimellä tai raaka-aineella

from flask import redirect, render_template, request, flash
from db import db
from sqlalchemy.sql import text

#TODO tietokanta muutokset reseptisivuille
#TODO varmistukset:käyttäjän oikeudet


def add_recipe(name, ingredients, instructions):
    sql = text("INSERT INTO recipes (name, instructions) VALUES (:name, :instructions) RETURNING id")
    result = db.session.execute(sql, {"name":name, "instructions":instructions})
    recipe_id = result.fetchone()[0]

    for ingredient in ingredients:
        # Check if ingredient exist in database
        result = db.session.execute("SELECT id FROM ingredients WHERE name = :name", {"name": ingredient["name"]}).fetchone()
        if result is None:
            # Add ingredient if not
            result = db.session.execute("INSERT INTO ingredients (name) VALUES (:name) RETURNING id", {"name": ingredient["name"]}).fetchone()
        ingredient_id = result[0]

        # Check if unit exist in database
        result = db.session.execute("SELECT id FROM units WHERE name = :name", {"name": ingredient["unit"]}).fetchone()
        if result is None:
            # Add unit if not 
            result = db.session.execute("INSERT INTO units (name) VALUES (:name) RETURNING id", {"name": ingredient["unit"]}).fetchone()
        unit_id = result[0]
    
    db.session.execute("INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit_id) VALUES (:recipe_id, :ingredient_id, :amount, :unit_id)", {"recipe_id": recipe_id, "ingredient_id": ingredient_id, "amount": ingredient["amount"], "unit_id": unit_id})

    db.session.commit()


def validate_input(input_string, input, min_length, max_length):
    if not input_string:
        raise ValueError(f"{input}-kenttä ei voi olla tyhjä!")
    elif len(input_string) < min_length:
        raise ValueError(f"Hieman liian lyhyt {input}-kenttä! Anna vähintään {min_length} merkkiä.")
    elif len(input_string) > max_length:
        raise ValueError(f"Nyt meni {input}-kenttä pitkäksi! Maksimipituus on {max_length} merkkiä.")
    return input_string


def get_recipe(name):
    sql = text("SELECT name, ingredients, instructions FROM recipes WHERE name = :name")
    result = db.session.execute(sql, {"name": name}).fetchone()
    return result
    
    
def list_recipes():
    sql = text("SELECT name FROM recipes ORDER BY id DESC")
    result = db.session.execute(sql).fetchall()
    return result    
    
    


