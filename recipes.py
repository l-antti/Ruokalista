from flask import redirect, render_template, request, flash, session
from db import db
from sqlalchemy.sql import text
import random



def add_ingredient(name):
    result = db.session.execute(text("SELECT id FROM ingredients WHERE name = :name"), {"name": name}).fetchone()
    if result is None:
        result = db.session.execute(text("INSERT INTO ingredients (name) VALUES (:name) RETURNING id"), {"name": name}).fetchone()
    else:
        db.session.execute(text("UPDATE ingredients SET name = :name WHERE id = :id"), {"name": name, "id": result[0]})
    return result[0]


def add_unit(unit):
    result = db.session.execute(text("SELECT id FROM units WHERE unit = :unit"), {"unit": unit}).fetchone()
    if result is None:
        raise ValueError(f"Mittayksikköä {unit} ei löydy tietokannasta.")
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


def edit_recipe(id, recipename, ingredients, instructions):
    try:
        db.session.begin()
        # Update the recipe details
        sql = text("UPDATE recipes SET recipename = :recipename, instructions = :instructions WHERE id = :id")
        db.session.execute(sql, {"recipename": recipename, "instructions": instructions, "id": id})
        # Delete the old ingredients
        sql = text("DELETE FROM recipe_ingredients WHERE recipe_id = :id")
        db.session.execute(sql, {"id": id})
        # Add the new ingredients
        for ingredient in ingredients:
            ingredient_name = ingredient["name"]
            ingredient_unit = ingredient["unit"] 
            ingredient_id = add_ingredient(ingredient_name)
            unit_id = add_unit(ingredient_unit)
            
            # Update the ingredient and unit details
            sql = text("UPDATE ingredients SET name = :name WHERE id = :id")
            db.session.execute(sql, {"name": ingredient_name, "id": ingredient_id})
            sql = text("UPDATE units SET unit = :unit WHERE id = :id")
            db.session.execute(sql, {"unit": ingredient_unit, "id": unit_id})
            
            db.session.execute(text("INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit_id) VALUES (:recipe_id, :ingredient_id, :amount, :unit_id)"), {"recipe_id": id, "ingredient_id": ingredient_id, "amount": ingredient["amount"], "unit_id": unit_id})
        db.session.commit()
        flash("Reseptin päivitys onnistui!")
    except Exception as e:
        db.session.rollback()
        flash("Virhe reseptin päivityksessä: " + str(e))
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
    # Convert ingredients list to a list of objects and sort by name
    ingredients_list = [{"name": i, "amount": ri, "unit": u} for i, ri, u in ingredients]
    sorted_ingredients_list = sorted(ingredients_list, key=lambda x: x['name'])
    return {
        "id": recipe.id,
        "recipename": recipe.recipename,
        "instructions": recipe.instructions,
        "ingredients": sorted_ingredients_list
    }

    
 
def search_recipes(query):
    # Search by recipe name
    sql = text("SELECT id, recipename, instructions FROM recipes WHERE LOWER(recipename) LIKE LOWER(:query)")
    recipes = db.session.execute(sql, {"query": "%" + query + "%"}).fetchall()
    # Search by ingredient
    sql = text("""
        SELECT r.id, r.recipename, r.instructions 
        FROM recipes r
        JOIN recipe_ingredients ri ON r.id = ri.recipe_id
        JOIN ingredients i ON ri.ingredient_id = i.id
        WHERE LOWER(i.name) LIKE LOWER(:query)
    """)
    recipes_by_ingredient = db.session.execute(sql, {"query": "%" + query + "%"}).fetchall()
    # Combine the results
    recipes.extend(recipes_by_ingredient)
    # Remove duplicates
    recipes = list(set(recipes))
    # Fetch ingredients for each recipe
    for recipe in recipes:
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
        # Create a new dictionary for the recipe
        recipe_dict = {"id": recipe.id, "recipename": recipe.recipename, "instructions": recipe.instructions, "ingredients": ingredients_list}

        # Replace the original recipe with the new dictionary
        recipes[recipes.index(recipe)] = recipe_dict
    return recipes
 
    
def list_recipes():
    sql = text("SELECT id, recipename FROM recipes ORDER BY recipename DESC")
    result = db.session.execute(sql).fetchall()
    return result   
 
 
def get_favourite_recipes(id):
    sql = text("SELECT recipes.* FROM recipes JOIN user_recipes ON recipes.id = user_recipes.recipe_id WHERE user_recipes.user_id = :id")
    result = db.session.execute(sql, {"id": id}).fetchall()
    return result


def add_to_favourites(recipe_id, user_id):
    sql = text("SELECT * FROM user_recipes WHERE user_id = :user_id AND recipe_id = :recipe_id")
    result = db.session.execute(sql, {"user_id": user_id, "recipe_id": recipe_id}).fetchone()
    if result:
        flash("Resepti on jo suosikkilistallasi!")
        return

    sql = text("INSERT INTO user_recipes (user_id, recipe_id) VALUES (:user_id, :recipe_id)")
    db.session.execute(sql, {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()
    flash("Resepti lisätty suosikkeihin!")
    

def remove_from_favourites(recipe_id, user_id):
    sql = text("DELETE FROM user_recipes WHERE user_id = :user_id AND recipe_id = :recipe_id")
    db.session.execute(sql, {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()



def generate_weekly_menu():
    #Generates a weekly menu with random recipes for lunch and dinner.
    recipe_list = list_recipes()
    weekly_menu = {}
    leftovers = None
    for i in range(7):
        lunch = leftovers if leftovers else random.choice(recipe_list)
        dinner = random.choice(recipe_list)
        weekly_menu[i] = {
            "Lunch": {"id": lunch[0], "recipename": lunch[1]},
            "Dinner": {"id": dinner[0], "recipename": dinner[1]}
        }
        leftovers = dinner  # Save dinner as leftovers for the next day
    
    return weekly_menu

    
def weekdays():
    days = {
    0: 'Maanantai',
    1: 'Tiistai',
    2: 'Keskiviikko',
    3: 'Torstai',
    4: 'Perjantai',
    5: 'Lauantai',
    6: 'Sunnuntai'
}
    return days


def get_weekly_menu():
    weekly_menu = session.get('menu', recipes.generate_weekly_menu())
    return weekly_menu
    
    
def get_shopping_list(weekly_menu):
    shopping_list = {}
    for day, meals in weekly_menu.items():
        # Count only dinner 
        dinner_recipe = meals["Dinner"]
        recipe_id = dinner_recipe["id"]
        recipe = get_recipe(recipe_id)
        for ingredient in recipe['ingredients']:
            # Add ingredient in shopping list
            if ingredient['name'] not in shopping_list:
                shopping_list[ingredient['name']] = {
                    'amount': 0,
                    'unit': ingredient['unit']
                }
            shopping_list[ingredient['name']]['amount'] += ingredient['amount']
    
    # Sort the shopping list by ingredient name
    sorted_shopping_list_items = sorted(shopping_list.items(), key=lambda item: item[0])
    
    # Format the sorted shopping list items
    formatted_shopping_list_items = [f"{item}: {data['amount']} {data['unit']}" for item, data in sorted_shopping_list_items]
    return formatted_shopping_list_items


    



