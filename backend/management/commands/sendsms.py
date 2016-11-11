from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import Func
from django.utils.translation import ugettext as _
from twilio.rest import Client

from backend.models import Session

# Check for sessions 15-20 minutes before their starting time
NOTIFY_START = 15
NOTIFY_END = 20


class Timestamp(Func):
    def as_sqlite(self, compiler, connection):
        return super().as_sql(
            compiler, connection,
            function='CAST',
            template='%(function)s(strftime("%%%%s", %(expressions)s) AS NUMERIC)',
        )

    def as_postgresql(self, compiler, connection):
        return super().as_sql(
            compiler, connection,
            function='EXTRACT',
            template='%(function)s(EPOCH FROM %(expressions)s)',
        )

    def as_mysql(self, compiler, connection):
        return super().as_sql(
            compiler, connection,
            function='CAST',
            template='%(function)s(STR_TO_DATE(%(expressions)s, "%%%%sM %%%%sd %%%%sY %%%%sh:%%%%si%%%%sp"))',
        )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('session_id', type=int)

    def handle(self, *args, **options):
        session = Session.objects.filter(
            pk=options['session_id'],
            is_sms_sent=False
        ).first()

        if not session:
            return

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        for viewer in session.viewer_set.exclude(mobile=''):
            message = _('The session %(session)s you have bookmarked '
                        'is starting soon.' % {
                            'session': session.name,
                        })

            print('Sending SMS "%(message)s" to %(mobile)s' % {
                'mobile': viewer.mobile,
                'message': message,
            })

            client.messages.create(
                to=viewer.mobile,
                messaging_service_sid=settings.TWILIO_COPILOT_SID,
                body=message,
            )

        session.is_sms_sent = True
        session.save()
