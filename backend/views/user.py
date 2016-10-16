from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.views import JSONWebTokenAPIView

from backend.helper import get_token
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

        token = get_token(user)
        return Response({'token': token}, status=status.HTTP_201_CREATED)


@api_view
@permission_classes((AllowAny,))
def verify_email(request):
    pass


@api_view(('POST',))
@permission_classes
def resend_verification(request):
    pass


class UserDetail(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = UserJWTSerializer
