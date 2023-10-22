from app import app
from flask import redirect, render_template, request, session, abort
import re
from Data.database_commands import *
from secrets import token_hex as generate_csrf_token

@app.route("/")
def index():
    if 'user_id' in session:
        project_info_list = get_all_project_info(session["user_id"])
        return render_template("index.html", project_info_list=project_info_list)
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
    if user_id:
        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = generate_csrf_token()

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

@app.route('/submit', methods=['POST'])
def submit():
    user_id = int(session["user_id"])
    project_name = request.form.get('project_name')
    project_description = request.form.get('project_description')
    project_name = request.form.get('project_name')
    project_description = request.form.get('project_description')

    check_csrf_token()
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

@app.route('/select_project/<int:idea_id>', methods=['POST'])
def select_project(idea_id):
    check_csrf_token()
    user_id = int(session["user_id"])
    select_idea(user_id, idea_id, selected=True)
    return redirect('/ideas')

@app.route('/bookmark_project/<int:idea_id>', methods=['POST'])
def bookmark_project(idea_id):
    check_csrf_token()
    user_id = int(session["user_id"])
    select_idea(user_id, idea_id, bookmarked=True)
    return redirect('/ideas')

@app.route('/edit_project/<int:idea_id>', methods=['GET'])
def edit_project(idea_id):
    user_id = int(session["user_id"])
    idea_info = get_project_info(idea_id, user_id)
    return render_template('edit_project.html', idea_info=idea_info)

@app.route("/update_project", methods=["POST"])
def update_project():
    check_csrf_token()
    
    user_id = int(session["user_id"])
    idea_id = int(request.form.get("idea_id"))
    project_url = request.form.get("project_url")
    grade = request.form.get("grade")
    idea_info = get_project_info(idea_id, user_id)

    if not project_url and grade:
        return render_template("edit_project.html", error="You cannot insert a grade without a project URL.", idea_info=idea_info)

    mark_completed(idea_id, user_id, project_url, grade)
    return redirect('/')

def check_csrf_token():
    if session["csrf_token"] != request.form["csrf_token"]:
        print("Aborting!")
        abort(403)

def is_valid_username(username):
    pattern = r"^[a-zA-Z0-9_]{3,20}$"
    if re.match(pattern, username):
        return True
    return False


if __name__ == "__main__":
    app.run(debug=True)
