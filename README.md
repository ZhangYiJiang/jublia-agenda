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


[django]: https://www.djangoproject.com/
[rest-framework]: http://www.django-rest-framework.org/
