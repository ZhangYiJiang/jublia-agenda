from django.conf.urls import url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm
from rest_framework_jwt.views import refresh_jwt_token

import backend.views.session_meta
from . import views

agenda_id = r'^(?P<agenda_id>[1-9][0-9]*)'

urlpatterns = [
    # For JWT authentication
    url(r'^users/auth', views.ObtainJSONWebToken.as_view(), name='auth'),
    url(r'^users/refresh', refresh_jwt_token),

    # User create, retrieve, update, verification, password reset
    url(r'^users/sign_up', views.sign_up, name='sign_up'),
    url(r'^users/me', views.UserDetail.as_view(), name='user'),

    url(r'users/verify/(\w+)', views.verify_email, name='verify_email'),
    url(r'users/verify$', views.resend_verification, name='resend_verification'),

    url(r'^users/password', password_reset, name='password_reset'),
    url(r'^users/password_done', password_reset_done, name='password_reset_done'),
    # TODO: Need to redirect the user to the homepage with the JWT. Probably need to rewrite
    # or wrap the  password_reset_confirm view
    url(r'users/reset', password_reset_confirm, name='password_reset_confirm'),

    # Agenda listing, detail
    url(r'^agenda', views.AgendaList.as_view(), name='agenda_list'),
    url(r'^(?P<pk>[1-9][0-9]*)$', views.AgendaDetail.as_view(), name='agenda_detail'),

    # Session listing, detail
    url(agenda_id + r'/sessions/(?P<pk>[1-9][0-9]*)',
        views.SessionDetail.as_view(), name='session_detail'),
    url(agenda_id + r'/sessions$',
        views.SessionList.as_view(), name='session_list'),

    # Session speakers
    url(agenda_id + r'/speakers/(?P<pk>[1-9][0-9]*)',
        backend.views.session_meta.SpeakerDetail.as_view(), name='speaker_detail'),
    url(agenda_id + r'/speakers$',
        backend.views.session_meta.SpeakerList.as_view(), name='speaker_list'),

    # Session tracks
    url(agenda_id + r'/tracks/(?P<pk>[1-9][0-9]*)',
        backend.views.session_meta.TrackDetail.as_view(), name='track_detail'),
    url(agenda_id + r'/tracks$',
        backend.views.session_meta.TrackList.as_view(), name='track_list'),

    # Session venues
    url(agenda_id + r'/venues/(?P<pk>[1-9][0-9]*)',
        backend.views.session_meta.VenueDetail.as_view(), name='venue_detail'),
    url(agenda_id + r'/venues$',
        backend.views.session_meta.VenueList.as_view(), name='venue_list'),

]
