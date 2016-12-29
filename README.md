# A\*genda

API Document: http://docs.jubliaagenda.apiary.io/ 

## Frontend documentation 

The frontend is written with Angular 2. See https://github.com/ZhangYiJiang/jublia-agenda/tree/master/frontend for more details. 

## Backend Setup 

The backend uses [Django 1.10][django] and [Django Rest Framework 3.4][rest-framework]. On development environment by default it will use a Sqlite database, and all mails are sent to log. To run the unit tests the database user will need permission to create databases (this is not necessary for the Sqlite database). 

To setup: 

1. Make sure you have prerequisites installed - Python 3.5 
2. Clone the repository 
3. Setup virtualenv - `pyvenv venv` 
4. Activate the virtualenv - `source venv/bin/activate` 
5. Install dependencies - `pip install -r requirements.txt` 
6. Edit environment settings - `cp jublia/env.py.example jublia/env.py` then `vim jublia/env.py` and update the `SECRET_KEY` (use http://www.miniwebtool.com/django-secret-key-generator/)
7. Return to the project root and run `./manage.py migrate` to run the DB migrations
8. Run the backend test suite using `./manage.py test backend`. Check that there are no errors.  
9. Start the server with `./manage.py runserver`
10. Make sure that there are no errors, then open `localhost:8000/admin` to check that Django is working properly
11. Use `./manage.py createsuperuser` to create a new admin account

## Commands 

Django comes with a number of useful [command line commands][commands] through `manage.py`. In addition, [Django Extensions][extensions] is also installed, which means there's a number of useful commands in addition to Django's defaults. Run `manage.py` without any commands to see a list. 
 
In addition to this we also define the following commands: 

### `seed` - seed database with fake data for testing 

This command will create a new user and generate a new event agenda with tracks, speakers and sessions for testing purposes. The following options are available. 

- `--user=None` - if specified, adds the seeded event to the user with the given email 
- `--tracks=2` - number of session tracks 
- `--speakers=5` - number of speakers 
- `--sessions=20` - number of sessions. 
- `--venues=3` - number of venues

The sessions are randomly assigned fields, speakers and tracks. Their timing should be within office hours, but no checks for overlapping sessions is done 

## Deployment 
 
Deployment to the staging server is done using the included [Fabric][fabric] script. The included commands are 

- **`frontend`** - Pull and build the frontend code 

- **`backend`** - Pull and build the backend code 

- **`deploy`** - Pull and deploy both the front and backend code 

- **`seed`** - Runs the database seed command. Use a colon to separate the arguments, which are passed straight to the command, like this `fab seed:'--sessions=30'`

[django]: https://www.djangoproject.com/
[rest-framework]: http://www.django-rest-framework.org/
[commands]: https://docs.djangoproject.com/en/1.10/ref/django-admin/#available-commands
[extensions]: https://django-extensions.readthedocs.io/
[fabric]: http://www.fabfile.org/installing.html
