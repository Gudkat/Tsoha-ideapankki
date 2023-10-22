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
        idea (tuple): Tuple of the idea and username.
    '''

    command = text("""
        SELECT ideas.idea_id, ideas.user_id, users.username, ideas.project_name, ideas.description
        FROM ideas
        JOIN users ON ideas.user_id = users.user_id
        WHERE ideas.idea_id=:idea_id
    """)
    result = db.session.execute(command, {"idea_id": idea_id})
    idea = result.fetchone()
    return idea

def select_idea(user_id, idea_id, selected=False, bookmarked=False):
    '''
    Links user with idea in the table "user_idea_link".

    Parameters:
        user_id (int): User ID of the individual.
        idea_id (int): Idea ID of the idea.
        selected (bool): True if the user has selected the idea, False if not.
        bookmarked (bool): True if the user has bookmarked the idea, False if not.
    '''

    # If the row exists in database, update the bookmarked and selected values. 
    # If not, create a new row.
    command = text("""
        INSERT INTO user_idea_link (user_id, idea_id, selected, bookmarked)
        VALUES (:user_id, :idea_id, :selected, :bookmarked)
        ON CONFLICT (user_id, idea_id)
        DO UPDATE SET selected=:selected, bookmarked=:bookmarked
        """)
    
    try:
        db.session.execute(command, {"user_id": user_id, "idea_id": idea_id, "selected": selected, "bookmarked": bookmarked})
        db.session.commit()
    except Exception as e:
        print("Error:", e)

def is_idea_completed(idea_id, user_id):
    '''
    Checks if the idea is marked completed for the current user.

    Parameters:
        idea_id (int): Idea ID of the idea.
        user_id (int): User ID of the individual.
    
    Returns:
        idea_completed (bool): True if the idea is marked completed for the current user, False if not.    
    '''

    command = text("""
        SELECT EXISTS (
                   SELECT * 
                   FROM completed_projects
                   WHERE idea_id=:idea_id AND user_id=:user_id
            )
        """)
    result = db.session.execute(command, {"idea_id": idea_id, "user_id": user_id})
    idea_completed = result.fetchone()[0]
    return idea_completed

def get_project_info(idea_id, user_id):
    '''
    Gets information for the project.

    Parameters:
        idea_id (int): Idea ID of the idea.
        user_id (int): User ID of the individual.

    Returns:
        project_info (tuple): Tuple of the project information.
    '''

    command = text("""
        SELECT 
            ideas.idea_id,
            ideas.project_name,
            ideas.description,
            user_idea_link.selected,
            user_idea_link.bookmarked,
            completed_projects.project_url,
            completed_projects.grade
        FROM ideas
        LEFT JOIN user_idea_link ON ideas.idea_id = user_idea_link.idea_id
        LEFT JOIN completed_projects ON ideas.idea_id = completed_projects.idea_id AND user_idea_link.user_id = completed_projects.user_id
        WHERE ideas.idea_id = :idea_id AND user_idea_link.user_id = :user_id;
        """)
    result = db.session.execute(command, {"idea_id": idea_id, "user_id": user_id})
    project_info = result.fetchone()
    return project_info

def get_all_project_info(user_id):
    '''
    Gets information for all the projects linked to a specific user.

    Parameters:
        user_id (int): User ID of the individual.

    Returns:
        project_info_list (list): List of tuples, each containing project information.
    '''

    command = text("""
        SELECT 
            ideas.idea_id,
            ideas.project_name,
            ideas.description,
            user_idea_link.selected,
            user_idea_link.bookmarked,
            completed_projects.project_url,
            completed_projects.grade,
            CASE 
                WHEN completed_projects.idea_id IS NOT NULL AND completed_projects.user_id IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS completed
        FROM user_idea_link
        LEFT JOIN ideas ON user_idea_link.idea_id = ideas.idea_id
        LEFT JOIN completed_projects ON user_idea_link.idea_id = completed_projects.idea_id AND user_idea_link.user_id = completed_projects.user_id
        WHERE user_idea_link.user_id = :user_id;
        """)

    result = db.session.execute(command, {"user_id": user_id})
    project_info_list = result.fetchall()
    return project_info_list

def mark_completed(idea_id, user_id, project_url=None, grade=None):
    '''
    Marks the project as completed for the user.

    Parameters:
        idea_id (int): Idea ID of the idea.
        user_id (int): User ID of the individual.
        project_url (str): URL of the project.
        grade (int): Grade of the project.
    '''

    command = text("""
        INSERT INTO completed_projects (idea_id, user_id, project_url, grade)
        VALUES (:idea_id, :user_id, :project_url, :grade)
        ON CONFLICT (idea_id, user_id)
        DO UPDATE SET project_url=:project_url, grade=:grade
        """)
    try:
        db.session.execute(command, {"idea_id": idea_id, "user_id": user_id, "project_url": project_url, "grade": grade})
        db.session.commit()
    except Exception as e:
        print("Error:", e)


#ChatGPT v.4 gave the basic structure for the docstring format and was used to check and make small adjustments the what they became in the end
#ChatGPT v.4 helped partially with the formatting of the code
