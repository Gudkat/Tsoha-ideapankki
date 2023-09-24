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




#ChatGPT v.4 gave the basic structure for the docstring format and was used to check and make small adjustments the what they became in the end
#ChatGPT v.4 helped partially with the formatting of the code
