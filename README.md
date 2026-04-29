# Django News Application Capstone

## Overview
This project is a Django-based news application that allows users to create, manage, and view articles and newsletters. It includes role-based permissions and a RESTful API with authentication.

## Features
- Custom user roles: Reader, Journalist, Editor
- Article creation and approval system
- Newsletter creation and management
- Role-based access control using Django groups
- REST API built with Django REST Framework
- JWT authentication for API access
- Automated unit tests
- MariaDB database integration

## Technologies Used
- Python
- Django
- Django REST Framework
- MariaDB (MySQL)
- PyMySQL

## Setup Instructions
1. Install dependencies:
   pip install -r requirements.txt

2. Run migrations:
   python manage.py migrate

3. Create a superuser:
   python manage.py createsuperuser

4. Run the development server:
   python manage.py runserver

## API Authentication
JWT authentication is implemented. Obtain a token at:
http://127.0.0.1:8000/api/token/

## Database
This project uses MariaDB instead of SQLite. The database configuration is defined in:
news_project/settings.py

## Notes
- The `venv` folder is excluded from submission.
- SQLite database files are not included since MariaDB is used.