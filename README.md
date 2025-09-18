# django-hw2

## Setup

Create and activate virtual environment:

```bash
cd .. && virtualenv venv && .\venv\Scripts\activate && cd mywebsite
```

## Running the Server

To start the development server:

```bash
cd mywebsite
python manage.py runserver
```

## Database Management

### Applying Model Changes

When models are modified, run the following commands to migrate:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Admin User

To create a new superuser for the admin interface:

```bash
python manage.py createsuperuser
```
