CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    class TEXT,
    instructions TEXT,
    ingredients TEXT
);
CREATE TABLE user_recipes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes
);
CREATE TABLE ingridients (
    id SERIAL PRIMARY KEY,
    name TEXT
);
CREATE TABLE recipe_ingridients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    ingridient_id INTEGER REFERENCES ingridients,
    amount INTEGER,
    measure_id INTEGER REFERENCES measures
);    
CREATE TABLE measures (
    id SERIAL PRIMARY KEY,
    name TEXT      
);
