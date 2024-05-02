#users module
# käyttäjän luominen, kirjautuminen sisään ja ulos, käyttäjän tietojenhallinta

from flask import redirect, render_template, request, session, flash
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
    
    
def login_user(username, password):
    sql = text("SELECT id, password, admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        return False
    if not check_password_hash(user.password, password):
        return False
	    
    session["user_id"] = user.id
    session["username"] = username
    session["logged_in"] = True
    session["is_admin"] = user.admin  # Tallenna käyttäjän rooli istuntoon
    return True


def is_admin():
    return session.get('is_admin', False)


def is_user():
    return 'logged_in' in session and session['logged_in']	    
		
		    
def user_id():
    return session.get("user_id", 0)   
   
def logout_user():
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]
    session["logged_in"] = False  
    
def get_profile(id):
    sql = text("SELECT * FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result
    

def create_user(username, password, password2):
    if validator(username, password, password2) == True:
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    return False
    
    
def validator(username, password, password2):
    if not password == password2:
        flash("Yritä uudelleen! Salasanat eivät täsmää")
        return False
    if len(password) < 6 or len(password) > 25:
        flash("Yritä uudelleen! Salasanassa tulee olla 7-24 merkkiä")
        return False
    if len(username) < 3 or len(username) > 19: 
        flash("Yritä uudelleen! Käyttäjätunnuksessa tulee olla 4-18 merkkiä")   
    if double_user(username) == False:
       flash("Yritä uudelleen! Käyttäjätunnus on jo käytössä")
       return False
       
    return True
    
             
def double_user(username):
    sql = text("SELECT username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return True
    return False

    
    
    
     
    

       
