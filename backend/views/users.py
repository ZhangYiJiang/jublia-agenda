from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serializers import UserSerializer

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@api_view
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(True):
        user = serializer.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token}, status=status.HTTP_201_CREATED)
