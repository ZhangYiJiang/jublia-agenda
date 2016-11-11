from django.conf import settings
from django.db.transaction import atomic
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Viewer, Agenda, Session
from backend.serializers import ViewerSerializer
from .base import AgendaContextMixin


@api_view(('POST',))
@permission_classes((AllowAny,))
def create_viewer(request, agenda_id):
    serializer = ViewerSerializer(data=request.data, context={
        'agenda': get_object_or_404(Agenda, pk=agenda_id),
    })

    serializer.is_valid(True)
    viewer = serializer.save()
    return Response({'token': viewer.token}, status=status.HTTP_201_CREATED)


@require_GET
def create_demo_viewer(request):
    agenda = Agenda.objects.get(pk=139)
    viewer = Viewer.objects.create(agenda=agenda)
    url = settings.BASE_URL + 'public/agenda/' + str(agenda.pk) + '/' + viewer.token + '?demo=1'
    return redirect(url)


def get_viewer(agenda_id, token):
    return get_object_or_404(Viewer, agenda=agenda_id, token=token)


class ViewerSessionList(AgendaContextMixin, RetrieveUpdateAPIView):
    serializer_class = ViewerSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_viewer(**self.kwargs)


class ViewerRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, agenda_id, token, session_id):
        # This is probably a little more convoluted than it should be
        # should refactor when there's time
        session = get_object_or_404(Session, pk=session_id, agenda=agenda_id)
        viewer = get_viewer(agenda_id, token)

        with atomic():
            reg, created = viewer.registration_set.get_or_create(session=session)
            if created:
                session.popularity = session.viewer_set.count()
                session.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, agenda_id, token, session_id):
        session = get_object_or_404(Session, pk=session_id, agenda=agenda_id)
        registration = get_object_or_404(session.registration_set, viewer__token=token)

        with atomic():
            registration.delete()
            session.popularity = session.viewer_set.count()
            session.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
