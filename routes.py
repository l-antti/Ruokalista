# routes module
# käsittelee sivupyynnöt

from app import app
from flask import Flask, render_template, request, redirect, flash, url_for
import users, recipes


# alkunäkymään kirjautuminen, lista resepteistä, linkki menun tekoon
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
    username = request.form.get("username")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    
    if users.create_user(username, password, password2) == False:
        return redirect(url_for("register")) 
    else:
        flash("Tilin luominen onnistui!")           
        return redirect(url_for("index"))
    
    
@app.route("/ruokalista", methods=["GET", "POST"])
def menu():
    pass
          
            
@app.route("/new_recipe", methods=["GET", "POST"])
def new_recipe():
    if request.method == "GET":
        return render_template("new_recipe.html")
    if request.method == "POST":
        name = request.form.get("name")
        ingredients = request.form.get("ingredients")
        instructions = request.form.get("instructions")
        recipes.add_recipe(name, ingredients, instructions)
        if recipes.add_recipe(name, ingredients, instructions):
            flash("Reseptin lisäys onnistui!")           
            return redirect(url_for("recipe_page", name=name))
        else:
           return render_template("error.html", message="Jotain meni pieleen :(") 
    
    
@app.route("/reseptit", methods=["GET"])
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

    
    
    
