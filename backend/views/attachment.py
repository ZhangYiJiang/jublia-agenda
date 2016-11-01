from rest_framework.generics import CreateAPIView

from backend.serializers import FileSerializer, ImageSerializer


class UserFileMixin:
    def get_queryset(self):
        return self.request.user.profile.attachment_set


class UploadFile(UserFileMixin, CreateAPIView):
    serializer_class = FileSerializer


class UploadImage(UserFileMixin, CreateAPIView):
    serializer_class = ImageSerializer
