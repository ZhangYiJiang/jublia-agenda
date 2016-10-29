import random
from datetime import timedelta

from django.utils.datetime_safe import date, datetime
from faker import Faker

fake = Faker()

today = date.today()
now = datetime.now()
later = now + timedelta(hours=2)
next_month = now + timedelta(days=30)


def user(data=None, full=False):
    if data is None:
        data = {}

    user = {
        'username': fake.email(),
        'password': fake.password(),
    }

    if full:
        user['company'] = fake.company()

    return {**user, **data}


def agenda(data=None, full=False):
    if data is None:
        data = {}

    agenda = {
        'name': fake.text(max_nb_chars=50),
    }

    if full:
        agenda = {
            **agenda,
            'description': fake.paragraph(),
            'location': fake.street_address(),
            'start_at': next_month.date().isoformat(),
            'website': fake.url(),
            # This needs to be high to avoid clashing with the session timing
            'duration': random.randint(6, 8),
        }

    return {**agenda, **data}


def session(data=None, full=False):
    if data is None:
        data = {}

    session = {
        'name': fake.text(max_nb_chars=160).split('.')[0],
    }

    if full:
        session = {
            **session,
            'description': '\n'.join(fake.paragraphs()),
            # Between 9am day one and 6pm day 6 at 15 min interval
            'start_at': random.randint(9 * 4, (6 * 24 + 18) * 4) * 15,
            # 30 min to 4 hours
            'duration': random.randint(2, 4 * 4) * 15,
        }

    return {**session, **data}


def speaker(data=None, full=False):
    if data is None:
        data = {}

    speaker = {
        'name': fake.name(),
        'company': fake.company(),
        'position': fake.job(),
        'email': fake.email(),
    }

    if full:
        speaker = {
            **speaker,
            'phone_number': fake.phone_number(),
            'company_description': fake.catch_phrase(),
            'company_url': fake.url(),
        }

    return {**speaker, **data}


def track(data=None):
    if data is None:
        data = {}

    track = {
        'name': fake.bs(),
    }
    return {**track, **data}


def venue(data=None, full=False):
    if data is None:
        data = {}

    venue = {
        'name': fake.secondary_address(),
    }

    if full:
        venue['unit'] = '#' + fake.bothify(text="##-##?")

    return {**venue, **data}


def viewer(data=None):
    if data is None:
        data = {}

    viewer = {
        'email': fake.email(),
    }

    return {**viewer, **data}


def category(data=None):
    if data is None:
        data = {}

    category = {
        'name': fake.bs(),
    }

    return {**category, **data}


def tag(data=None):
    if data is None:
        data = {}

    tag = {
        'name': fake.bs()
    }

    return {**tag, **data}
