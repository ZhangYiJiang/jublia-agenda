from collections import OrderedDict
from datetime import timedelta

from django.db.models import Count, F
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.models import Agenda
from backend.permissions import IsAgendaOwner


@api_view(('GET',))
@permission_classes((IsAgendaOwner,))
def analytics(request, agenda_id):
    agenda = get_object_or_404(Agenda.objects, pk=agenda_id)
    date_query = agenda.viewer_set.annotate(
        session=F('registration__session'),
        date=TruncDate('registration__created_at'),
    ).exclude(session=None)
    today = timezone.now().date()
    limit = today - timedelta(days=14)

    cumulative = date_query.filter(date__lte=limit).values('session').annotate(count=Count('session'))
    session_cumulative = {}
    for row in cumulative:
        session_cumulative[row['session']] = row['count']

    rows = date_query.order_by('date').filter(date__gt=limit)\
        .values('session', 'date').annotate(count=Count('pk'))
    data = {}
    for session in agenda.session_set.values_list('pk', flat=True):
        data[session] = OrderedDict()
        date = limit + timedelta(days=1)
        while date <= today:
            data[session][date.isoformat()] = session_cumulative.get(session, 0)
            date += timedelta(days=1)

    for row in rows:
        data[row['session']][row['date'].isoformat()] += row['count']

    return Response(data, status=status.HTTP_200_OK)
