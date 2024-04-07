# recipe module
# uusien reseptien lisääminen, selaus, reseptien etsiminen nimellä tai raaka-aineella

from flask import redirect, render_template, request, flash
from db import db
from sqlalchemy.sql import text

#TODO raaka-aineiden muokkaus erilliseen tietokantaan+mahdollisuus lisätä enemmän tai vähemmän kuin kolme
#TODO varmistukset: syötteeen pituus ja käyttäjän oikeudet
#TODO tuplausten estäminen
def add_recipe(name, ingredients, instructions):
    sql = text("INSERT INTO recipes (name, ingredients, instructions) VALUES (:name, :ingredients, :instructions)")
    db.session.execute(sql, {"name":name, "ingredients":ingredients, "instructions":instructions})
    db.session.commit()
    return True
   
    
def list_recipes():
    sql = text("SELECT name FROM recipes ORDER BY id DESC")
    result = db.session.execute(sql)
    recipes = result.fetchall()
    return recipes
    
def get_recipe(name):
    sql = text("SELECT name, ingredients, instructions FROM recipes WHERE name = :name")
    result = db.session.execute(sql, {"name": name})
    recipe = result.fetchone()
    return recipe
    

