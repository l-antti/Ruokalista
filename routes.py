# routes module
# käsittelee sivupyynnöt

from app import app
from flask import Flask, render_template, request, redirect, flash, url_for
import users, recipes
from recipes import validate_input



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")
        
        
@app.route("/login/check", methods=["POST"])        
def login_check():
    username = request.form["username"]
    password = request.form["password"]
    if users.login_user(username, password):
        flash("Kirjautuminen onnistui!")
        return redirect(url_for("index"))
    else:
        flash("Kirjautuminen epäonnistui. Väärä käyttäjätunnus tai salasana")
        return redirect(url_for("login"))
        
           
@app.route("/logout")
def logout():
    users.logout_user()
    flash("Nähdään taas!")
    return redirect(url_for("index"))
         
                 
@app.route("/register")
def register():
    return render_template("create_user.html")
      
      
@app.route("/register/check", methods=["POST"])      
def register_check():
    try:
        username = validate_input(request.form["username"], "Käyttäjänimi", 3, 12)
        password = request.form["password"]
        password2 = request.form["password2"]
        
        if users.create_user(username, password, password2) == False:
            return redirect(url_for("register")) 
        else:
            flash("Tilin luominen onnistui! Kirjaudu sisään nähdäksesi enemmän.")           
            return redirect(url_for("login"))
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("register"))
 
            
@app.route("/new_recipe")
def new_recipe():
    return render_template("new_recipe.html")
    
    
@app.route("/new_recipe/add", methods=["POST"])      
def add_new_recipe():
    try:
        name = validate_input(request.form.get("name"), "reseptin nimi", 3, 50)
        instructions = validate_input(request.form.get("instructions"),"valmistusohje", 5, 500)
        
        ingredient_names = [validate_input(name, "raaka-aine", 3, 50) for name in request.form.getlist("ingredientName")]
        ingredient_amounts = [validate_input(amount, "määrä", 1, 10) for amount in request.form.getlist("ingredientAmount")]
        ingredient_units = [validate_input(unit, "yksikkö", 1, 20) for unit in request.form.getlist("ingredientUnit")]
        
        # Combine ingredients into a list of dictionaries
        ingredients = [{"name": n, "amount": a, "unit": u} for n, a, u in zip(ingredient_names, ingredient_amounts, ingredient_units)]

        flash("Reseptin lisäys onnistui!")           
        return redirect(url_for("recipe_page", name=name))  
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("new_recipe"))
    
@app.route("/reseptit")
def browse_recipes():
    recipe_list = recipes.list_recipes()
    return render_template("list_recipes.html", recipes=recipe_list)
 
 
@app.route("/recipe_page/<path:name>")
def recipe_page(name):
    recipe = recipes.get_recipe(name)
    if recipe is None:
        flash("Reseptiä ei löytynyt!")
        return redirect(url_for("index"))
    return render_template("recipe_page.html", recipe=recipe)


@app.route("/ruokalista", methods=["GET", "POST"])
def menu():
    pass
             
    
    
