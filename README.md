# Jublia Agenda 

API Document: http://docs.jubliaagenda.apiary.io/ 

## Backend Setup 

The backend uses [Django 1.10][django] and [Django Rest Framework 3.4][rest-framework]. To setup: 

1. Make sure you have prerequisites installed - Python 3.5 
2. Clone the repository 
3. Setup virtualenv - `pyvenv venv` 
4. Activate the virtualenv - `source venv/bin/activate` 
5. Install dependencies - `pip install -r requirements.txt` 
6. Edit environment settings - `cp jublia/env.py.example jublia/env.py` then `vim jublia/env.py` and update the `SECRET_KEY` (use http://www.miniwebtool.com/django-secret-key-generator/)
7. Return to the project root and run `python manage.py migrate` to run the DB migrations
8. Start the server with `python manage.py runserver`
9. Make sure that there are no errors, then open `localhost:8000/admin` to check that Django is working properly
10. Use `python manage.py createsuperuser` to create a new admin account

## Deployment 
 
Deployment to the staging server is done using the included [Fabric][fabric] script. The included commands are 

- **`frontend`** - Pull and build the frontend code 

- **`backend`** - Pull and build the backend code 

- **`deploy`** - Pull and deploy both the front and backend code 

[django]: https://www.djangoproject.com/
[rest-framework]: http://www.django-rest-framework.org/
[fabric]: http://www.fabfile.org/installing.html
