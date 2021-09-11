from django.apps import AppConfig


class CastInviteeDetailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cast_invitee_details'

class UserMailConfig(AppConfig):
    name = 'cast_invitee_details'

    def ready(self):
        import cast_invitee_details.signals
