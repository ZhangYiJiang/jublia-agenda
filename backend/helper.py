from django.apps import apps
from django.conf import settings
from django.utils.crypto import get_random_string
from icalendar import Calendar
from rest_framework_jwt.settings import api_settings
from twilio.rest import Client

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_token(user):
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


def calendar():
    cal = Calendar()
    cal.add('method', 'publish')
    cal.add('version', '2.0')
    cal.add('prodid', r'//Jublia//Jublia Agenda//EN')

    return cal


def get_twilio_client():
    return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


class UniqueTokenGenerator:
    def __init__(self, model, length=20, field='token'):
        self.length = length
        self.model = model
        self.field = field

    def __call__(self, *args, **kwargs):
        Model = apps.get_model('backend', self.model)
        token = get_random_string(self.length)
        while Model.objects.filter(**{self.field: token}).count() > 0:
            token = get_random_string(self.length)
        return token

    def deconstruct(self):
        args = (self.model,)
        kwargs = {
            'length': self.length,
            'field': self.field,
        }
        return 'backend.helper.UniqueTokenGenerator', args, kwargs
