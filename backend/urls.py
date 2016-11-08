from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import refresh_jwt_token

from . import views

agenda_id = r'(?P<agenda_id>[1-9][0-9]*)/'

router = SimpleRouter()
router.register(agenda_id + r'categories/(?P<category_id>[1-9][0-9]*)/tags',
                views.TagViewSet)
router.register(agenda_id + r'categories', views.CategoryViewSet)

urlpatterns = [
    # For JWT authentication
    url(r'^users/auth$', views.ObtainJSONWebToken.as_view(), name='auth'),
    url(r'^users/refresh$', refresh_jwt_token),

    # User create, retrieve, update, verification, password reset
    url(r'^users/sign_up$', views.sign_up, name='sign_up'),
    url(r'^users/me$', views.UserDetail.as_view(), name='user'),

    url(r'^users/verify/(\w+)$', views.verify_email, name='verify_email'),
    url(r'^users/verify$', views.resend_verification, name='resend_verification'),

    url(r'^users/password$', password_reset, name='password_reset'),
    url(r'^users/password/done$', password_reset_done, name='password_reset_done'),
    # Note that this view below uses our own password_reset_complete
    url(r'^users/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^users/reset/done$', password_reset_complete, name='password_reset_complete'),

    # File upload endpoints
    url(r'^uploads/image$', views.UploadImage.as_view(), name='upload-image'),

    # Demo route
    url(r'demo', views.create_demo_viewer, name='demo'),

    # Session listing, detail
    url(agenda_id + r'sessions/(?P<pk>[1-9][0-9]*)/calendar$',
        views.SessionCalendar.as_view(), name='session-calendar'),
    url(agenda_id + r'sessions/(?P<pk>[1-9][0-9]*)$',
        views.SessionDetail.as_view(), name='session_detail'),
    url(agenda_id + r'sessions$',
        views.SessionList.as_view(), name='session_list'),

    # Session speakers
    url(agenda_id + r'speakers/(?P<pk>[1-9][0-9]*)$',
        views.session_meta.SpeakerDetail.as_view(), name='speaker_detail'),
    url(agenda_id + r'speakers$',
        views.session_meta.SpeakerList.as_view(), name='speaker_list'),

    # Session tracks
    url(agenda_id + r'tracks/(?P<pk>[1-9][0-9]*)$',
        views.session_meta.TrackDetail.as_view(), name='track_detail'),
    url(agenda_id + r'tracks$',
        views.session_meta.TrackList.as_view(), name='track_list'),

    # Session venues
    url(agenda_id + r'venues/(?P<pk>[1-9][0-9]*)$',
        views.session_meta.VenueDetail.as_view(), name='venue_detail'),
    url(agenda_id + r'venues$',
        views.session_meta.VenueList.as_view(), name='venue_list'),
    
    # Session analytics
    url(agenda_id + 'data$', views.analytics, name='analytics'),
    url(agenda_id + 'dirty$', views.AgendaDirtySession.as_view(), name='dirty_sessions'),

    # Agenda viewers
    url(agenda_id + r'viewers/(?P<token>\w+)/calendar$',
        views.ViewerCalendar.as_view(), name='viewer-calendar'),
    url(agenda_id + r'viewers/(?P<token>\w+)/(?P<session_id>[1-9][0-9]*)$',
        views.ViewerRegistrationView.as_view(), name='viewer_registration'),
    url(agenda_id + r'viewers/(?P<token>\w+)$',
        views.ViewerSessionList.as_view(), name='viewer_sessions'),
    url(agenda_id + r'viewers$', views.create_viewer, name='viewer_create'),

    # Agenda listing, detail
    url(r'^agendas$', views.AgendaList.as_view(), name='agenda_list'),
    url(agenda_id + r'calendar$', views.AgendaCalendar.as_view(), name='agenda-calendar'),
    url(r'^(?P<pk>[1-9][0-9]*)$', views.AgendaDetail.as_view(), name='agenda_detail'),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
