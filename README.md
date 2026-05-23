# Django News Application Capstone

## Description

This project is a Django-based News Application developed for the HyperionDev Software Engineering Bootcamp.

The application allows:
- Readers to view articles and newsletters
- Journalists to create and manage articles and newsletters
- Editors to approve pending articles
- Users to subscribe to journalists and publishers

The project uses:
- Django
- Django REST Framework
- MariaDB/MySQL
- Django permissions and groups
- API endpoints
- Sphinx documentation

---

## Features

### Reader Permissions
- View articles
- View newsletters
- Subscribe to publishers
- Subscribe to journalists

### Journalist Permissions
- Create articles
- Edit articles
- Delete articles
- Create newsletters
- Edit newsletters
- Delete newsletters

### Editor Permissions
- View pending articles
- Approve pending articles
- Manage published content

---

## Installation

### 1. Clone the repository

```bash
git clone <repository_url>

git clone <repository_url>

### 2. Navigate into the project folder

cd Django-News-Application-Capstone

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure MariaDB/MySQL

Update the database settings in:

news_project/settings.py

Example configuration:

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': 'news_db',
'USER': 'root',
'PASSWORD': 'root123',
'HOST': '127.0.0.1',
'PORT': '3306',
}
}

### Create the MariaDB Database

Before running migrations, create the database manually in HeidiSQL or MariaDB.

The database should be named:

    news_db

In HeidiSQL:
1. Connect to MariaDB using the root user.
2. Right-click in the database list.
3. Select Create new > Database.
4. Enter the database name:

    news_db

5. Click OK.

After the database has been created, run:

    python manage.py makemigrations
    python manage.py migrate

### 5. Run migrations

python manage.py makemigrations

python manage.py migrate

### 6. Run the server

python manage.py runserver

---

## Running Tests

Run the following command:

python manage.py test

---

## API Endpoint

Article approval API endpoint:

/api/approved/

---

## Diagrams Included

The project includes:

* Use Case Diagram
* Class Diagram
* Sequence Diagram

These diagrams are located in the diagrams folder.

---

## Documentation

Sphinx documentation is included in the docs/build/html directory.

Open:

docs/build/html/index.html

to view the documentation.

---

## Author

Spencer McNamara