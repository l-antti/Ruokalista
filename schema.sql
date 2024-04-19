CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN DEFAULT false
);
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    recipename TEXT,
    instructions TEXT 
);
CREATE TABLE user_recipes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes
);
CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT
);    
CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    unit TEXT 
);
CREATE TABLE recipe_ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    ingredient_id INTEGER REFERENCES ingredients,
    amount INTEGER,
    unit_id INTEGER REFERENCES units
);  
  
INSERT INTO units (unit) VALUES ('g'), ('kpl'), ('ml'), ('rkl'), ('tl');     

