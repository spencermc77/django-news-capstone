# Django News Application Capstone

## Description

This project is a Django-based News Application developed for the HyperionDev Software Engineering Bootcamp.

The application allows:

- Readers to view articles and newsletters
- Journalists to create and manage articles and newsletters
- Editors to approve pending articles
- Users to subscribe to journalists and publishers

Technologies used:

- Django
- Django REST Framework
- MariaDB / MySQL
- Docker
- Sphinx Documentation
- Django Permissions and Groups

---

# Features

## Reader Permissions

- View articles
- View newsletters
- Subscribe to publishers
- Subscribe to journalists

## Journalist Permissions

- Create articles
- Edit articles
- Delete articles
- Create newsletters
- Edit newsletters
- Delete newsletters

## Editor Permissions

- View pending articles
- Approve pending articles
- Manage published content

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/spencermc77/django-news-capstone.git
cd django-news-capstone
```

## 2. Create a Virtual Environment

Create and activate a virtual environment before installing dependencies.

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

## 4. Configure Database

This project uses MariaDB/MySQL.

Update database settings inside:

```text
news_project/settings.py
```

Example configuration:

```python
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
```

Create a database named:

```text
news_db
```

## 5. Run Migrations

Run migrations before starting the server:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Run Application Locally

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

---

# Docker Setup

The Dockerfile is located in the root directory.

## Build Docker Image

```bash
docker build -t django-news-app .
```

## Database Configuration for Docker

Docker containers run in isolated environments.

If MariaDB is running locally on Windows, update:

```python
'HOST': 'host.docker.internal'
```

instead of:

```python
'HOST': '127.0.0.1'
```

This allows Docker containers to connect to MariaDB running on the host machine.

If running MariaDB in another container, replace HOST with the database container name.

## Run Migrations Before Docker Startup

Ensure the database exists and migrations have already been applied:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run Docker Container

```bash
docker run -p 8000:8000 django-news-app
```

Open:

```text
http://127.0.0.1:8000
```

---

# Running Tests

Run:

```bash
python manage.py test
```

---

# API Endpoint

Article approval endpoint:

```text
/api/approved/
```

---

# Diagrams Included

Project diagrams include:

- Use Case Diagram
- Class Diagram
- Sequence Diagram

Location:

```text
diagrams/
```

---

# Documentation

Sphinx documentation is located at:

```text
docs/build/html/index.html
```

Open this file in a browser to view generated documentation.

---

# Author

Spencer McNamara