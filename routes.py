# routes module
# käsittelee sivupyynnöt

from app import app
from flask import Flask, render_template, request, redirect, flash, url_for, session
import users, recipes
from form_processing import validate_input, process_form_data
from flask_wtf.csrf import CSRFError



@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return "CSRF-tarkistus epäonnistui. Yritä uudelleen.", 400

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
        username = request.form["username"]
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
    # Retrieve form data from session if it exists
    form_data = session.get('form_data', {})
    return render_template("new_recipe.html", form_data=form_data)
    
    
@app.route("/new_recipe/add", methods=["POST"])      
def add_new_recipe():
    try:
        recipename, ingredients, instructions = process_form_data(request.form)
        recipe = recipes.add_recipe(recipename, ingredients, instructions)
        return redirect(url_for("new_recipe"))  
    except ValueError as e:
        flash(str(e))
        session.pop('form_data', None)
        
        return redirect(url_for("new_recipe"))

    
@app.route("/recipes")
def browse_recipes():
    recipe_list = recipes.list_recipes()
    return render_template("list_recipes.html", recipes=recipe_list)
 
 
@app.route("/recipe_page/<int:id>")
def recipe_page(id):
    recipe = recipes.get_recipe(id)
    if recipe is None:
        flash("Reseptiä ei löytynyt!")
        return redirect(url_for("index"))
    return render_template("recipe_page.html", recipe=recipe)


@app.route("/search")
def search():
    query = request.args.get("query")
    recipe_list = recipes.search_recipes(query)
    return render_template("search.html", recipes=recipe_list)


@app.route("/menu")
def menu_view():
    menu = recipes.weekly_menu()
    return render_template("menu.html", weekly_menu=menu)


@app.route("/menu/generate", methods=["POST"])
def generate_menu():
    recipes.generate_weekly_menu()
    return redirect(url_for("menu_view"))
             
    
    
