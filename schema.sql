CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ideas (
    idea_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    project_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_idea_link (
    user_id INTEGER REFERENCES users(user_id),
    idea_id INTEGER REFERENCES ideas(idea_id),
    PRIMARY KEY(user_id, idea_id),
    bookmarked BOOLEAN DEFAULT FALSE,
    selected BOOLEAN DEFAULT FALSE
);

CREATE TABLE completed_projects (
    idea_id INTEGER REFERENCES ideas(idea_id), 
    user_id INTEGER REFERENCES users(user_id),
    project_url VARCHAR(2048),
    grade VARCHAR(10),
    date_completed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (idea_id, user_id),
    CONSTRAINT check_grade_if_url
        CHECK ((project_url IS NOT NULL AND grade IS NOT NULL) OR (project_url IS NULL AND grade IS NULL))
);
-- completed_projects not tested yet

-- ChatGPT v4 translated my python code to create the tables to schema.sql file 