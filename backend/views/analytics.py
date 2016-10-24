from collections import OrderedDict

from django.db.models import Count, F
from django.db.models.functions import TruncDate
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
    rows = agenda.viewer_set.annotate(
        date=TruncDate('registration__created_at'),
        session=F('registration__session')
    ).exclude(date=None, session=None).order_by('date').values('session', 'date').annotate(count=Count('pk'))

    data = {}

    for session in agenda.session_set.values_list('pk', flat=True):
        data[session] = OrderedDict()

    for row in rows:
        data[row['session']][row['date'].isoformat()] = row['count']

    return Response(data, status=status.HTTP_200_OK)
