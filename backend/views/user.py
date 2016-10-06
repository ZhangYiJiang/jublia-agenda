from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from backend.helper import get_token
from backend.serializers import UserSerializer


@api_view(('POST',))
@permission_classes((AllowAny,))
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(True):
        user = serializer.save()
        token = get_token(user)
        return Response({'token': token}, status=status.HTTP_201_CREATED)


class UserDetail(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
