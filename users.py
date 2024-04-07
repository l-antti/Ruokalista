#users module
# käyttäjän luominen, kirjautuminen sisään ja ulos, käyttäjän tietojenhallinta

from flask import redirect, render_template, request, session, flash
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
    
def login_user(username, password):
	sql = text("SELECT id, password FROM users WHERE username=:username")
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()    
	if not user:
	    return False
	else:
	    if check_password_hash(user.password, password):
		    session["user_id"] = user.id
		    session["username"]= username
		    return True
	    else:
		    return False
    
def logout_user():
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]

# TODO: no duplicate usernames
def create_user(username, password):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return True
    
def user_id():
    return session.get("user_id", 0)
       
