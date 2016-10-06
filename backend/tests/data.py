from datetime import timedelta
from django.utils.datetime_safe import date, datetime

today = date.today()
now = datetime.now()
later = now + timedelta(hours=2)

user = {
    'email': 'test@example.com',
    'password': 'password12345',
}

agenda = {
    'name': 'Test Conf. 2016',
}

full_agenda = {
    **agenda,
    'location': 'Test Hotel',
    'description': """Sint velit eveniet. Rerum atque repellat voluptatem quia
    rerum. Numquam excepturi beatae sint laudantium consequatur. Magni occaecati
    itaque sint et sit tempore. Nesciunt amet quidem. Iusto deleniti cum autem
    ad quia aperiam.""",
    'date': today.isoformat(),
}

session = {
    'name': 'The Real Story Behind JS Performance in Mobile Web and Hybrid Apps',
}

full_session = {
    **session,
    'description': """Sint velit eveniet. Rerum atque repellat voluptatem quia
    rerum. Numquam excepturi beatae sint laudantium consequatur. Magni occaecati
    itaque sint et sit tempore. Nesciunt amet quidem. Iusto deleniti cum autem
    ad quia aperiam.""",
    'start_at': now.isoformat(),
    'end_at': later.isoformat(),
}
