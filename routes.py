# routes module
# käsittelee sivupyynnöt

from app import app
from flask import Flask, render_template, request, redirect, flash, url_for, session, abort
import users, recipes
from form_processing import validate_input, process_form_data
from datetime import timedelta
import random, secrets

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=1)
    
@app.before_request
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")
        
        
@app.route("/login/check", methods=["POST"])        
def login_check():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
 
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
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
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
 
@app.route("/profile/<int:id>")
def profile(id):
    if not users.is_user():
        flash("Sinun täytyy olla kirjautunut sisään nähdäksesi tämän sivun.")
        return redirect(url_for("login"))
    allow = False
    if users.is_admin():
        allow = True
    elif users.user_id() == id:
        allow = True
    if allow:
        user = users.get_profile(id)
        favourites = recipes.get_favourite_recipes(id)
        return render_template("profile.html", user=user, favourite_recipes=favourites)
    else:
        flash("Ei oikeutta nähdä sivua")
        return redirect(url_for("index"))
        

@app.route('/add_to_favorites/<int:id>', methods=['POST'])
def add_to_favorites(id):
    if not users.is_user():
        flash("Sinun täytyy olla kirjautunut sisään lisätäksesi suosikkeja.")
        return redirect(url_for("login"))
    recipes.add_to_favourites(id, users.user_id())
    
    return redirect(url_for("recipe_page", id=id)) 



@app.route('/remove_from_favorites/<int:id>', methods=['POST'])
def remove_from_favorites(id):
    if not users.is_user():
        flash("Sinun täytyy olla kirjautunut sisään poistaaksesi suosikkeja.")
        return redirect(url_for("login"))
    recipes.remove_from_favourites(id, users.user_id())
    flash("Resepti poistettu suosikeista!")
    return redirect(url_for("profile", id=users.user_id()))

            
@app.route("/new_recipe")
def new_recipe():
    # Retrieve form data from session if it exists
    form_data = session.get('form_data', {})
    return render_template("new_recipe.html", form_data=form_data)
    
    
@app.route("/new_recipe/add", methods=["POST"])      
def add_new_recipe():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
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



@app.route("/recipe_page/<int:id>/edit")
def edit_recipes(id):
    if not users.is_admin():
        flash("Vain ylläpitäjät voivat muokata reseptejä!")
        return redirect(url_for("index"))
    
    # Get the recipe details
    recipe = recipes.get_recipe(id)
    if recipe is None:
        flash("Reseptiä ei löytynyt!")
        return redirect(url_for("index"))
    
    # Pass the recipe details to the template
    return render_template("edit_recipe_page.html", recipe=recipe)


@app.route("/recipe_page/<int:id>/edit_recipe", methods=["POST"])      
def edit_added_recipe(id):
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
    try:
        # Process the form data
        recipename, ingredients, instructions = process_form_data(request.form)
        
        # Call the function to update the recipe in the database
        recipes.edit_recipe(id, recipename, ingredients, instructions)
        
        flash("Resepti päivitetty onnistuneesti!")
        return redirect(url_for("recipe_page", id=id))
        
    except ValueError as e:
        flash(str(e))
        session.pop('form_data', None)
        
        return redirect(url_for("new_recipe"))    
   
    

@app.route("/search")
def search():
    query = request.args.get("query")
    recipe_list = recipes.search_recipes(query)
    return render_template("search.html", recipes=recipe_list)
    
    


@app.route("/menu/generate", methods=["POST"])
def generate_menu():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)
    menu = recipes.generate_weekly_menu()
    session['menu'] = menu
    session['weekdays'] = recipes.weekdays()
    return redirect(url_for("menu_view"))
    
@app.route("/menu")
def menu_view():
    menu = session.get('menu')
    recipes_list = recipes.list_recipes()
    weekdays = session.get('weekdays', recipes.weekdays()) 
    
    return render_template("menu.html", weekly_menu=menu, recipes=recipes_list, weekdays = weekdays)

@app.route("/menu/recipes")
def menu_recipes():
    recipe_list = recipes.list_recipes()
    return render_template("list_recipes.html", recipes=recipe_list)

@app.route("/generate_shopping_list")
def generate_shopping_list():
    weekly_menu = session.get('menu')
    shopping_list = recipes.get_shopping_list(weekly_menu)
    return render_template("shopping_list.html", shopping_list=shopping_list)




    
