
def create_users_table(cur):
    command = """
    CREATE TABLE users (generated the code above after being instru
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cur.execute(command)

def create_ideas_table(cur):
    command = """
    CREATE TABLE ideas (
        idea_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        project_name VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cur.execute(command)

def create_user_idea_link_table(cur):
    command = """
    CREATE TABLE user_idea_link (
        user_id INTEGER REFERENCES users(user_id),
        idea_id INTEGER REFERENCES ideas(idea_id),
        PRIMARY KEY(user_id, idea_id)
    )
    """
    cur.execute(command)

def create_completed_projects_table(cur):
    command = """
    CREATE TABLE completed_projects (
        project_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        project_url VARCHAR(2048) NOT NULL,
        grade VARCHAR(10),
        date_completed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cur.execute(command)

def create_all_tables(cur):
    create_users_table(cur)
    create_ideas_table(cur)
    create_user_idea_link_table(cur)
    create_completed_projects_table(cur)

def main(conn):
    with conn.cursor() as cur:
        create_all_tables(cur)
    conn.commit()

# ChatGPT wrote the code after being given multiple prompts