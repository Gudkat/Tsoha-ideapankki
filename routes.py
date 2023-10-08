from app import app
from flask import redirect, render_template, request, session
from sqlalchemy.sql import text
import re
from Data.database_commands import create_user, login, add_idea_to_db, get_ideas, get_idea_by_idea_id, select_idea


# index, login and logout are partially ripped from course webpage. I'll work on it myself later on I guess.
@app.route("/")
def index():
    if 'user_id' in session:
        return render_template("index.html")
    else:
        return redirect("/login")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/sign_up_validation", methods=["POST"])
def sign_up_validation():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    if is_valid_username(username):
        create_user(username, email, password)
        return redirect("/login")
    else:
        return render_template("sign_up.html", error="Invalid username. Username must be 3-20 characters long and can only contain letters, numbers and underscores.")

@app.route("/login")
def login_form():
    return render_template("login.html")


@app.route("/login_validation",methods=["POST"])
def login_validation():
    username = request.form["username"]
    password = request.form["password"]
    user_id = login(username, password)
    print(user_id)
    if user_id:
        session["username"] = username
        session["user_id"] = user_id
        return redirect("/")    
    else: 
        return render_template("login.html", error="Invalid username or password.")

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

@app.route('/idea_form')
def idea_form():
    return render_template('idea_form.html')

@app.route('/submit_idea', methods=['POST'])
def submit_idea():
    user_id = int(session["user_id"])
    project_name = request.form.get('project_name')
    project_description = request.form.get('project_description')
    add_idea_to_db(user_id, project_name, project_description)

    return render_template('submit.html', project_name=project_name, project_description=project_description)

@app.route('/submit', methods=['POST'])
def submit():
    user_id = int(session["user_id"])
    project_name = request.form.get('project_name')
    project_description = request.form.get('project_description')

    project_name = request.form.get('project_name')
    project_description = request.form.get('project_description')
    add_idea_to_db(user_id, project_name, project_description)

    return render_template('submit.html', project_name=project_name, project_description=project_description)

@app.route('/ideas')
def ideas():
    ideas = get_ideas()
    return render_template('ideas.html', ideas=ideas)

@app.route('/idea_<idea_id>')
def idea_page(idea_id):
    idea = get_idea_by_idea_id(idea_id)
    return render_template('individual_idea.html', idea=idea)

# @app.route('/ideas/<idea_id>', methods=['POST'])
# def select_idea(idea_id):
#     # Your logic here to mark the idea as selected for your personal project
#     return redirect(('ideas.html'))

@app.route('/select_project/<int:idea_id>', methods=['GET'])
def select_project(idea_id):
    user_id = int(session["user_id"])
    select_idea(user_id, idea_id)
    return redirect('/ideas')

def is_valid_username(username):
    pattern = r"^[a-zA-Z0-9_]{3,20}$"
    if re.match(pattern, username):
        return True
    return False


if __name__ == "__main__":
    app.run(debug=True)
