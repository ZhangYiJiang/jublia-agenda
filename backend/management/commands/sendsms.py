from datetime import timedelta

from django.core.management import BaseCommand
from django.db import models
from django.db.models import F, Func
from django.utils import timezone

from backend.helper import get_twilio_client
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
    def handle(self, *args, **options):
        notify_start = timezone.now() + timedelta(minutes=NOTIFY_START)
        notify_end = timezone.now() + timedelta(minutes=NOTIFY_END)
        start_time = Timestamp('agenda__start_at', output_field=models.IntegerField()) + (F('start_at') * 60)
        sessions = Session.objects.annotate(start_time=start_time).filter(
            is_sms_sent=False,
            agenda__published=True,
            start_time__gte=notify_start.timestamp(),
            start_time__lte=notify_end.timestamp(),
        ).prefetch_related('viewer_set').all()

        client = get_twilio_client()
        for session in sessions:
            for viewer in session.viewer_set.exclude(mobile=''):
                print('Sending SMS for %(session)s to %(mobile)s' % {
                    'mobile': viewer.mobile,
                    'session': session.name,
                })
            session.is_sms_sent = True
            session.save()
