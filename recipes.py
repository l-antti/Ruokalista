# recipe module
# uusien reseptien lisääminen, selaus, reseptien etsiminen nimellä tai raaka-aineella

from flask import redirect, render_template, request, flash, session
from db import db
from sqlalchemy.sql import text
import random



def add_ingredient(name):
    
    result = db.session.execute(text("SELECT id FROM ingredients WHERE name = :name"), {"name": name}).fetchone()
   
    if result is None:
        result = db.session.execute(text("INSERT INTO ingredients (name) VALUES (:name) RETURNING id"), {"name": name}).fetchone()
    
    return result[0]


def add_unit(unit):
    result = db.session.execute(text("SELECT id FROM units WHERE unit = :unit"), {"unit": unit}).fetchone()
    if result is None:
        result = db.session.execute(text("INSERT INTO units (unit) VALUES (:unit) RETURNING id"), {"unit": unit}).fetchone()
    return result[0]
    

def add_recipe(recipename, ingredients, instructions):
    try:
        db.session.begin()
        sql = text("INSERT INTO recipes (recipename, instructions) VALUES (:recipename, :instructions) RETURNING id")
        result = db.session.execute(sql, {"recipename":recipename, "instructions":instructions})
        recipe_id = result.fetchone()[0]

        for ingredient in ingredients:
            ingredient_name = ingredient["name"]
            ingredient_unit = ingredient["unit"] 
            ingredient_id = add_ingredient(ingredient_name)
            unit_id = add_unit(ingredient_unit)

            db.session.execute(text("INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit_id) VALUES (:recipe_id, :ingredient_id, :amount, :unit_id)"), {"recipe_id": recipe_id, "ingredient_id": ingredient_id, "amount": ingredient["amount"], "unit_id": unit_id})

        db.session.commit()
        flash("Reseptin lisäys onnistui!")
    except Exception as e:
        db.session.rollback()
        flash("Virhe reseptin lisäyksessä: " + str(e))
        
        # Save form data in session
        session['form_data'] = {
            'recipename': recipename,
            'ingredients': ingredients,
            'instructions': instructions
        }


        
def get_recipe(id):
    # Fetch recipe details
    sql = text("SELECT id, recipename, instructions FROM recipes WHERE id = :id")
    recipe = db.session.execute(sql, {"id": id}).fetchone()

    # If recipe does not exist, return None
    if recipe is None:
        return None

    # Fetch ingredients for the recipe
    sql = text("""
        SELECT i.name, ri.amount, u.unit 
        FROM recipe_ingredients ri 
        JOIN ingredients i ON ri.ingredient_id = i.id 
        JOIN units u ON ri.unit_id = u.id 
        WHERE ri.recipe_id = :recipe_id
    """)
    ingredients = db.session.execute(sql, {"recipe_id": recipe.id}).fetchall()

    # Convert ingredients list to a list of objects
    ingredients_list = [{"name": i, "amount": ri, "unit": u} for i, ri, u in ingredients]

    return {
        "recipename": recipe.recipename,
        "instructions": recipe.instructions,
        "ingredients": ingredients_list
    }
    
def list_recipes():
    sql = text("SELECT id, recipename FROM recipes ORDER BY recipename DESC")
    result = db.session.execute(sql).fetchall()
    return result    
    

def weekly_menu():
    menu = generate_weekly_menu()
    return menu

def generate_weekly_menu():
    #Generates a weekly menu with random recipes for lunch and dinner.
    recipe_list = list_recipes()
    weekly_menu = {}
    leftovers = None
    for i in range(7):
        lunch = leftovers if leftovers else random.choice(recipe_list)
        dinner = random.choice(recipe_list)
        weekly_menu[i] = {
            "Lunch": lunch,
            "Dinner": dinner
        }
        leftovers = dinner  # Save dinner as leftovers for the next day
    return weekly_menu
    


