CREATE DATABASE movie_db;

\c movie_db

CREATE SCHEMA postgers;

CREATE SCHEMA my_app;


CREATE TABLE postgers.movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    genre VARCHAR(100)
);

CREATE TABLE postgers.directors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_year INT
);

CREATE TABLE my_app.reviews (
    id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES postgers.movies(id),
    review_text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5)
);

CREATE TABLE my_app.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

SELECT nspname AS schema_name FROM pg_catalog.pg_namespace;

\dt postgers.*
\dt my_app.*


SET search_path TO postgers, my_app;

SELECT * FROM movies;
SELECT * FROM my_app.reviews;
