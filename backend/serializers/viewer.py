from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.models import Registration
from backend.models import Viewer
from .base import BaseSerializer, AgendaPrimaryKeyRelatedField


class RegistrationSerializer(BaseSerializer):
    viewer = AgendaPrimaryKeyRelatedField(klass='viewer')
    session = AgendaPrimaryKeyRelatedField(klass='session')

    class Meta:
        model = Registration
        fields = ('viewer', 'session',)


class ViewerSerializer(BaseSerializer):
    email = serializers.EmailField(required=True)
    sessions = AgendaPrimaryKeyRelatedField(klass='session', many=True, required=False)

    def validate_mobile(self, mobile):
        if mobile.startswith('65'):
            mobile = '+' + mobile
        elif not mobile.startswith('+'):
            mobile = '+65' + mobile

        if len(mobile) != 11 or mobile[3] not in ('8', '9'):
            raise ValidationError(_('%s does not appear to be a Singaporean mobile '
                                    'number' % mobile))
        return mobile

    def validate_email(self, email):
        existing = Viewer.objects.filter(email=email, agenda=self.context['agenda']).first()
        if existing:
            msg = _("This email has already been used. We have sent the link "
                    "to your personalized agenda to your email.")
            existing.send_agenda_email()
            raise ValidationError(msg)
        return email

    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        viewer = super().create(validated_data)
        viewer.send_agenda_email()
        return viewer

    class Meta:
        model = Viewer
        fields = ('email', 'mobile', 'sessions',)
