CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(100) NOT NULL,
    is_admin BOOLEAN NOT NULL
);