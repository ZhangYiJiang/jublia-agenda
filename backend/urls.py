from django.conf.urls import url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

import backend.views.session_meta
from . import views

urlpatterns = [
    # For JWT authentication
    url(r'^users/auth', obtain_jwt_token, name='auth'),
    url(r'^users/refresh', refresh_jwt_token),

    # User create, retrieve, update, password reset
    url(r'^users/sign_up', views.sign_up, name='sign_up'),
    url(r'^users/me', views.UserDetail.as_view(), name='user'),
    url(r'^users/password', password_reset, name='password_reset'),
    url(r'^users/password_done', password_reset_done, name='password_reset_done'),
    # TODO: Need to redirect the user to the homepage with the JWT. Probably need to rewrite
    # or wrap the  password_reset_confirm view
    url(r'users/reset', password_reset_confirm, name='password_reset_confirm'),

    # Agenda listing, detail
    url(r'^agenda', views.AgendaList.as_view(), name='agenda_list'),
    url(r'^(?P<pk>[1-9][0-9]*)$', views.AgendaDetail.as_view(), name='agenda_detail'),

    # Session listing, detail
    url(r'^(?P<agenda_id>[1-9][0-9]*)/sessions$',
        views.SessionList.as_view(), name='session_list'),
    url(r'^(?P<agenda_id>[1-9][0-9]*)/sessions/(?P<pk>[1-9][0-9]*)',
        views.SessionDetail.as_view(), name='session_detail'),

    # Session speakers
    url(r'^(?P<agenda_id>[1-9][0-9]*)/speakers$',
        backend.views.session_meta.SpeakerList.as_view(), name='speaker_list'),
    url(r'^(?P<agenda_id>[1-9][0-9]*)/speakers/(?P<pk>[1-9][0-9]*)',
        backend.views.session_meta.SpeakerDetail.as_view(), name='speaker_detail'),

]
