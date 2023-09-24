# Tsoha-ideapankki
This is a project for the course Tietokannat ja web-ohjelmointi (Database and web programming) at the University of Helsinki.

## Table of Contents

1. [Purpose of the Program](#purpose-of-the-program)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Current State](#current-state)

## Purpose of the Program

The purpose of the program is to allow users to share their ideas for possible projects for the course Tietokannat ja web-ohjelmointi. Other users can then vote for the ideas they like. Users can also select projects to work on. Once a project is completed, users can mark it as completed. User can share the completed projects to other users f.ex. with github links and if they wish, can share what grade the project recieved.

## Features

- **User Management**: Create, edit, and delete user profiles.
- **Idea Management**: Users can share their ideas for possible projects.
- **Project Selection**: Allows users to select projects based on various ideas.
- **Track Completed Projects**: Monitor projects that have been successfully completed.
- **Role-based Access**: Define roles for admin and normal user and assign them to users for different access levels.
- **Voting projects** Users can vote for projects they like or dislike. The projects will be shown in the order of most liked to least liked.

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
3. **User access** - 'User' can submit ideas, choose projects, mark their project completed and view projects that are completed. 'User' can also vote for projects and ideas.
4. **Admin access** - 'Admins' have all the same rights as 'Users'. In addition, 'Admins' can view all 'users' and their details. 'Admins' also have Role Management rights.

### Ideas

1. **Submit a New Idea** - Navigate to the 'Ideas' section and click on 'Submit New Idea'. Provide a title and description.
2. **Edit/Delete Idea** - 'Users' can edit or delete their ideas if nobody has chosen said project yet. Editing project will reset the vote count.
3. **Voting Ideas** - 'Users' can vote for ideas they like or dislike. The ideas will be shown in the order of most liked to least liked. Votes can't go below 0.

### Projects

1. **Choose a Project** - Browse the ideas available and select one to work on by clicking 'Choose This Idea'. The chosen idea will now be your 'Active project'.
2. **Marking a Project as Completed** - Once you've successfully completed a project, navigate to your projects list and select 'Mark as Completed' for the respective project.
3. **View Completed Projects** - Navigate to the 'Your Completed Projects' section to view all the projects you've completed. Navigate to the 'All Completed Projects' section to view all the projects completed by all users.
4. **Voting Projects** - Users can vote for projects they like or dislike. The projects will be shown in the order of most liked to least liked.

### Role Management

1. **Viewing User Roles** - Admins can view all user roles and their permissions in the 'Roles' section.
2. **Assigning Roles to Users** - Admins can assign specific roles to users, granting them permissions based on their role. Navigate to the 'User-Role Association' section, select a user, and assign a role.

## Current state
The program currently has the following features:
* Account creation
  * Account creation hashes passwords into database
* Account login
  * Saves user_id and username into session
* Submission of ideas
  * Ideas are saved into database
* Logging out
  * Logging out navigation is provided in the dummy page after submitting an idea
  * This will be edited later to be included in all pages
  * You can also logout by manually going to /logout page
  * Logging out deletes user_id and username from session
