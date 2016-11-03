from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Agenda
from backend.models import Session
from backend.models import Viewer
from backend.renderers import CalendarRenderer


class CalendarAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (CalendarRenderer,)

    def get_object(self, *args, **kwargs):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        return Response(self.get_object(request, *args, **kwargs))

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response['content-disposition'] = 'attachment'
        if hasattr(self, 'filename'):
            response['content-disposition'] += '; filename="%s.ics"' % self.filename
        return response


class SessionCalendar(CalendarAPIView):
    def get_object(self, request, agenda_id, pk):
        session = get_object_or_404(Session, pk=pk, agenda=agenda_id)
        self.filename = session.name
        return session


class AgendaCalendar(CalendarAPIView):
    def get_object(self, request, agenda_id):
        agenda = get_object_or_404(Agenda, pk=agenda_id)
        self.filename = agenda.name + ' schedule'
        return agenda


class ViewerCalendar(CalendarAPIView):
    def get_object(self, request, agenda_id, token):
        viewer = get_object_or_404(Viewer, agenda=agenda_id, token=token)
        self.filename = viewer.agenda.name + ''
        return viewer
