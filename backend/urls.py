from django.conf.urls import url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views

urlpatterns = [
    # For JWT authentication
    url(r'^users/auth', obtain_jwt_token),
    url(r'^users/refresh', refresh_jwt_token),

    url(r'^users/sign_up', views.sign_up),

    url(r'^users/password', password_reset),
    url(r'^users/password_done', password_reset_done, name='password_reset_done'),

    # TODO: Need to redirect the user to the homepage with the JWT. Probably need to rewrite
    # or wrap the  password_reset_confirm view
    url(r'users/reset', password_reset_confirm),
]
