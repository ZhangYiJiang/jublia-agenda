from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views

urlpatterns = [
    # For JWT authentication
    url(r'^users/auth', obtain_jwt_token),
    url(r'^users/refresh', refresh_jwt_token),
]
