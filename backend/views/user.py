from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset_confirm as reset_confirm
from django.shortcuts import redirect, get_object_or_404
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.views import JSONWebTokenAPIView

from backend.helper import get_token
from backend.models import Profile
from backend.serializers import BaseAgendaSerializer
from backend.serializers import UserSerializer, UserJWTSerializer


@sensitive_post_parameters()
@api_view(('POST',))
@permission_classes((AllowAny,))
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(True):
        user = serializer.save()

        # Create and attach a new agenda if 'event_name' is included in the
        # request so that the user can get started with the app immediately
        event_name = request.data.get('event_name')
        if event_name:
            agenda = BaseAgendaSerializer(data={'name': event_name}, context={'user': user})
            agenda.is_valid(True)
            agenda.save()

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
        raise ValidationError({'username': _('Username is required')})
    user = get_object_or_404(User, username=request.data['username'])
    user.profile.send_verification_email()
    return Response(status=status.HTTP_204_NO_CONTENT)


@sensitive_post_parameters()
def password_reset_confirm(request, *args, **kwargs):
    # Django forces the user to reauthenticate after resetting password. We don't want
    # this behavior, but the user object is encapsulated in the original view function,
    # and we don't want to copy the entire method, so we use the same method the original
    # uses to get the user object and replace the 3XX redirect response with our own
    response = reset_confirm(request, *args, **kwargs)
    if response.status_code in range(300, 400):
        # Code taken from the auth.views.password_reset_confirm method
        uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
        user = User.objects.get(pk=uid)
        return redirect('/?token=' + get_token(user))
    return response


class UserDetail(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = UserJWTSerializer
