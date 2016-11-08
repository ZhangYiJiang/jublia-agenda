from django.conf import settings
from django.core.mail import send_mass_mail
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Agenda
from backend.permissions import IsOwnerOrReadOnly, IsAgendaOwner
from backend.serializers import BaseAgendaSerializer, AgendaSerializer
from .base import UserContextMixin


class AgendaList(UserContextMixin, ListCreateAPIView):
    serializer_class = BaseAgendaSerializer

    def get_serializer_context(self):
        # Add tracks to the serializer context, if it is in the request
        context = super().get_serializer_context()
        context['tracks'] = self.request.data.get('tracks', [])
        return context

    def get_queryset(self):
        return Agenda.objects.filter(profile__user=self.request.user)


class AgendaDetail(UserContextMixin, RetrieveUpdateDestroyAPIView):
    queryset = Agenda.objects.prefetch_related('session_set', 'venue_set', 'speaker_set', 'track_set')

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = AgendaSerializer


class SlugAgendaDetail(AgendaDetail):
    lookup_field = 'slug'


class AgendaDirtySession(APIView):
    permission_classes = (IsAgendaOwner,)

    def get(self, request, agenda_id):
        agenda = get_object_or_404(Agenda, pk=agenda_id)
        sessions = agenda.session_set.filter(is_dirty=True).exclude(popularity=0)\
            .values('id', 'popularity')
        return Response(sessions, status.HTTP_200_OK)

    def post(self, request, agenda_id):
        agenda = get_object_or_404(Agenda, pk=agenda_id)
        viewers = agenda.viewer_set.filter(sessions__is_dirty=True)\
            .distinct().prefetch_related('sessions')
        template = get_template('email/session_update.html')
        title = _('%s - Some sessions you have bookmarked have changed' % agenda.name)

        mail = []
        for viewer in viewers:
            body = template.render({
                'sessions': viewer.sessions.filter(is_dirty=True)
            })

            mail.append((title, body, settings.DEFAULT_FROM_EMAIL, [viewer.email]))
        agenda.session_set.filter(is_dirty=True).update(is_dirty=False)

        data = {
            'sent': send_mass_mail(mail, fail_silently=False),
        }
        return Response(data, status=status.HTTP_200_OK)
