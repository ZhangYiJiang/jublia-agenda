from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from backend import serializers
from backend.models import Category
from backend.models import Tag
from backend.models import Track, Speaker, Venue
from backend.permissions import IsAgendaOwnerOrReadOnly
from .base import AgendaContextMixin


class TrackList(AgendaContextMixin, ListCreateAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = serializers.BaseTrackSerializer

    def get_queryset(self):
        return Track.objects.filter(agenda=self.kwargs['agenda_id'])


class TrackDetail(AgendaContextMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = serializers.TrackSerializer

    def get_queryset(self):
        return Track.objects.filter(agenda=self.kwargs['agenda_id'])


class SpeakerList(AgendaContextMixin, ListCreateAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = serializers.BaseSpeakerSerializer

    def get_queryset(self):
        return Speaker.objects.filter(agenda=self.kwargs['agenda_id'])


class SpeakerDetail(AgendaContextMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = serializers.SpeakerSerializer

    def get_queryset(self):
        return Speaker.objects.filter(agenda=self.kwargs['agenda_id'])


class VenueList(AgendaContextMixin, ListCreateAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = serializers.BaseVenueSerializer

    def get_queryset(self):
        return Venue.objects.filter(agenda=self.kwargs['agenda_id'])


class VenueDetail(AgendaContextMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = serializers.VenueSerializer

    def get_queryset(self):
        return Venue.objects.filter(agenda=self.kwargs['agenda_id'])


class CategoryViewSet(AgendaContextMixin, ModelViewSet):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tags'] = self.request.data.get('tags', [])
        return context

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateCategorySerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return self.queryset.filter(agenda=self.kwargs['agenda_id'])


class TagViewSet(AgendaContextMixin, ModelViewSet):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializers = serializers.TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        return self.queryset.filter(agenda=self.kwargs['agenda_id'],
                                    category=self.kwargs['category_id'])
