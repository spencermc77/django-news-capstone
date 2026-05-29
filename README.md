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
- Docker

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

    git clone https://github.com/spencermc77/django-news-capstone.git
    cd django-news-capstone

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Configure the database

This project uses MariaDB/MySQL.

Update the database settings in:

    news_project/settings.py

Example database settings:

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

Create a MariaDB database named:

    news_db

Run migrations:

    python manage.py makemigrations
    python manage.py migrate

### 4. Run the application locally

    python manage.py runserver

Open the application in a browser:

    http://127.0.0.1:8000

---

## Docker Setup

Build the Docker image:

    docker build -t django-news-app .

Run the Docker container:

    docker run -p 8000:8000 django-news-app

Open the application in a browser:

    http://127.0.0.1:8000

Notes:

- This project uses MariaDB/MySQL.
- If running locally, MariaDB should be running before migrations.
- If running through Docker, database networking or external database configuration may be required.
- The Dockerfile is located in the root directory of this repository.

---

## Running Tests

Run the test suite:

    python manage.py test

---

## API Endpoint

Article approval endpoint:

    /api/approved/

---

## Diagrams Included

The project includes:

- Use Case Diagram
- Class Diagram
- Sequence Diagram

These diagrams are located in:

    diagrams/

---

## Documentation

Sphinx documentation is located in:

    docs/build/html/index.html

Open this file to view the documentation.

---

## Author

Spencer McNamara