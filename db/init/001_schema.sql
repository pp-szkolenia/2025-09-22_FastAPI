\connect task_manager;


CREATE TABLE IF NOT EXISTS tasks
(
    id SERIAL PRIMARY KEY,
    description VARCHAR(30) NOT NULL,
    priority SMALLINT,
    is_completed BOOLEAN NOT NULL
);


CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(100) NOT NULL,
    is_admin BOOLEAN NOT NULL
);
