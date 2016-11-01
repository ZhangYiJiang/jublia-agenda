from rest_framework.generics import CreateAPIView

from backend.serializers import AttachmentSerializer


class UploadImage(CreateAPIView):
    def get_queryset(self):
        return self.request.user.profile.attachment_set

    serializer_class = AttachmentSerializer
