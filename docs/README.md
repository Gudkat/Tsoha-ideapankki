# Tsoha-ideapankki
This is a project for the course Tietokannat ja web-ohjelmointi (Database and web programming) at the University of Helsinki.

## Table of Contents

1. [Purpose of the Program](#purpose-of-the-program)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Current State](#current-state)
6. [Current Issues](#current-issues)
7. [Use of AI](#use-of-ai)
8. [Future Plans](#future-plans)


## Purpose of the Program

The purpose of the program is to allow users to share their ideas for possible projects for the course Tietokannat ja web-ohjelmointi. Other users can then vote for the ideas they like. Users can also select projects to work on. Once a project is completed, users can mark it as completed. User can share the completed projects to other users f.ex. with github links and if they wish, can share what grade the project recieved.

## Features

- **Idea Management**: Users can share their ideas for possible projects.
- **Project Selection**: Allows users to select projects based on various ideas.
- **Track Completed Projects**: Monitor projects that have been successfully completed.

## Installation
1. Clone the repository
```bash
git clone git@github.com:Gudkat/Tsoha-ideapankki.git
```
2. Create and activate virtual environment
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Define the schema for the database
```bash
psql < schema.sql
```
5. Run posgresql database
6. Run the python script to create .env file
```bash
setup_env.py
``` 
5. run the Flask app in the project directory with command
```bash
flask run
```

## Usage

### User Registration & Access

1. **Register** - New users can create an account. New users are assigned the 'User' role by default. If no other users exist, the first user will be assigned the 'Admin' role.
2. **Login** - Users can log in with their credentials to access their accounts.
3. **User access** - 'User' can submit ideas, choose projects, mark their project completed and view projects that are completed. 

### Ideas

1. **Submit a New Idea** - User can create new idea for a project by navigating to 'New Idea'. New idea requires for user to provide a title and a description.

### Projects

1. **Choose a Project** - Browse the ideas available and select one or more ideas to work on by clicking 'Select Project' under 'Browse Ideas' section. The chosen idea will be viewed as 'Active project' under 'My Prjojects' section.
2. **Marking a Project as Completed** - Once user has successfully completed a project, user can go to 'My Projects' and click 'edit idea'. There user can mark the project as completed and provide a link to the source of the project and mark which grade they recieved for hte project. Source and grade are optional and can be edited later.
3. **View Completed Projects** - View completed projects in 'My Projects' section. 

## Use of AI
[How AI has been used in the project](https://github.com/Gudkat/Tsoha-ideapankki/blob/main/docs/use_of_ai.md)

## Future plans
* Add admin features
  - 'Admins' have all the same rights as 'Users'. In addition, 'Admins' can view all 'users' and their details. 'Admins' also have Role Management rights.
  - 'Admins' can delete users
  - 'Admins' can delete ideas
  - 'Admins' can delete projects
  - 'Admins' can give other users admin rights

* Add upvoting/downvoting features for projects
 - Users can vote for projects they like or dislike. The projects will be shown in the order of most liked to least liked.
