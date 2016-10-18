from backend.serializers import *


def create_user(data):
    s = UserSerializer(data=data)
    s.is_valid(raise_exception=True)
    user = s.save()
    # Mark the user as verified for convenience
    user.profile.is_verified = True
    user.profile.save()
    return user


def create_agenda(user, data):
    s = AgendaSerializer(data=data, context={'user': user})
    s.is_valid(True)
    return s.save()


def create_session(agenda, data):
    s = SessionSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()


def create_speaker(agenda, data):
    s = SpeakerSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()


def create_track(agenda, data=None):
    if data is None:
        data = {}
    s = TrackSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()


def create_venue(agenda, data):
    s = VenueSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()


def create_viewer(agenda, data):
    s = ViewerSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()


class ErrorDetailMixin:
    def assertIsErrorDetail(self, detail):
        self.assertIsInstance(detail, dict)
        for v in detail.values():
            self.assertFalse(isinstance(v, str))
            for s in v:
                self.assertIsInstance(s, str)
