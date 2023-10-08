from sqlalchemy.sql import text
from db import db
from werkzeug.security import check_password_hash, generate_password_hash


def create_user( username: str, email: str, password: str):
    '''
    Creates new user in the database.

    Parameters:
        username (str): Username of the individual.
        email (str): Email of the individual.
        password (str): Password of the individual.    
    '''


    command = text("""
        INSERT INTO users (username, email, password)
        VALUES (:username, :email, :password)
        """)
    
    password = generate_password_hash(password)
    db.session.execute(command, {"username": username, "email": email, "password": password})
    db.session.commit()

def login(username: str, password: str):
    '''
    Checks if the user exists in the database and if the password matches the username.

    Parameters:
        user_name (str): Username of the individual.
        password (str): Password of the individual.

    Returns:
        user_id (int): User ID of the individual. 
        If the user does not exist, returns None. 
        If the password does not match the username, returns None.
    '''

    command = text("""
        SELECT user_id, password FROM users
        WHERE username=:username
        """)
    result = db.session.execute(command, {"username": username})
    user_id = result.fetchone()
    if user_id == None:
        return None # If the user does not exist, returns None.
    else:
        if check_password_hash(user_id[1], password):
            return user_id[0]    
    
    return None # If the password does not match the username, returns None.

def add_idea_to_db(user_id: int, project_name: str, description: str):
    '''
    Adds a user's project idea to the database.

    Parameters:
        user_id (int): User ID of the individual submitting the idea.
        project_name (str): Name of the project.
        description (str): Description of the project.
    '''

    command = text("""
        INSERT INTO ideas (user_id, project_name, description)
        VALUES (:user_id, :project_name, :description)
        """)
    try:
        db.session.execute(command, {"user_id": user_id, "project_name": project_name, "description": description})
        db.session.commit()
        print("Idea added to the database")
    except Exception as e:
        print("Error:", e)

def get_ideas():
    '''
    Gets all the ideas from the database.

    Returns:
        ideas (list): List of all the ideas in the database.
    '''

    command = text("""
        SELECT idea_id, user_id, project_name, description FROM ideas
        """)
    result = db.session.execute(command)
    ideas = result.fetchall()
    return ideas

def get_idea_by_idea_id(idea_id):
    '''
    Gets the idea from the database by the idea ID.

    Returns:
        idea (tuple): Tuple of the idea.
    '''

    command = text("""
        SELECT idea_id, user_id, project_name, description FROM ideas
        WHERE idea_id=:idea_id
        """)
    result = db.session.execute(command, {"idea_id": idea_id})
    idea = result.fetchone()
    return idea

def select_idea(user_id, idea_id):
    print(user_id, idea_id)
    '''
    Links user with idea in the table "user_idea_link".

    Parameters:
        user_id (int): User ID of the individual.
        idea_id (int): Idea ID of the idea.
    '''

    command = text("""
        INSERT INTO user_idea_link (user_id, idea_id)
        VALUES (:user_id, :idea_id)
        """)
    
    try:
        db.session.execute(command, {"user_id": user_id, "idea_id": idea_id})
        db.session.commit()
        print("Idea selected")
    except Exception as e:
        print("Error:", e)


#ChatGPT v.4 gave the basic structure for the docstring format and was used to check and make small adjustments the what they became in the end
#ChatGPT v.4 helped partially with the formatting of the code
