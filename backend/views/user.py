from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.views import JSONWebTokenAPIView

from backend.helper import get_token
from backend.models import Profile
from backend.serializers import UserSerializer, UserJWTSerializer


@api_view(('POST',))
@permission_classes((AllowAny,))
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(True):
        user = serializer.save()

        # Create and attach a new agenda if 'event_name' is included in the
        # request so that the user can get started with the app immediately
        if 'event_name' in request.data:
            user.profile.agenda_set.create(name=request.data['event_name'])

        return Response(status=status.HTTP_201_CREATED)


@api_view()
@permission_classes((AllowAny,))
def verify_email(request, token):
    profile = get_object_or_404(Profile, verification_token=token)
    if profile.verify_email(request):
        return redirect('/?token=' + get_token(profile.user))
    else:
        return _('Your verification email has expired. We have sent you another one. Please check your email.')


@api_view(('POST',))
@permission_classes((AllowAny,))
def resend_verification(request):
    if 'username' not in request.data:
        raise ValidationError(_('Email is required'))
    user = get_object_or_404(User, username=request.data['username'])
    user.profile.send_verification_email()
    return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = UserJWTSerializer
