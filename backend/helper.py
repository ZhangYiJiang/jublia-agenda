from django.apps import apps
from django.utils.crypto import get_random_string
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_token(user):
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


def generate_unique_token(model, length=20, field='token'):
    def generate():
        Model = apps.get_model('backend', model)
        token = get_random_string(length)
        while Model.objects.filter(**{field: token}).count() > 0:
            token = get_random_string(length)
        return token
    return generate
