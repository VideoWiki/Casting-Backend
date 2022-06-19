from .models import CastInviteeDetails
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.global_variable import CLIENT_DOMAIN_URL
from bbb_api.create_event_email_sender import attendee_mail

@receiver(post_save, sender=CastInviteeDetails)
def post_save_emailer(sender, instance, created, **kwargs):

    if created:
        print(instance.cast.event_name, instance.name, instance.role, instance.email)
        meeting_url = CLIENT_DOMAIN_URL + "/e/{}/".format(instance.cast.public_meeting_id)
        a_password = instance.cast.attendee_password
        m_password = instance.cast.moderator_password
        v_password = instance.cast.viewer_password
        vw_stream = instance.cast.bbb_stream_url_vw
        dt = instance.cast.schedule_time
        date = dt.date()
        hour = dt.hour
        min = dt.minute
        schedule_time = str(date) + " at " + str(hour) + ":" + str(min) + " GMT"
        print(instance.role, "ppp")
        send_otp = instance.cast.send_otp
        if vw_stream == None:
            stream_url = ""
        else:
            stream_url = "{}/live/{}".format(CLIENT_DOMAIN_URL,instance.cast.public_meeting_id)
        if instance.role == "participant":
            send_mail_invite = attendee_mail(instance.name,
                                             instance.email,
                                             instance.cast.event_name,
                                             schedule_time,
                                             meeting_url,
                                             a_password,
                                             stream_url,
                                             instance.role,
                                             send_otp
                                             )
        elif instance.role == "spectator":
            send_mail_invite = attendee_mail(instance.name,
                                             instance.email,
                                             instance.cast.event_name,
                                             schedule_time,
                                             meeting_url,
                                             a_password,
                                             stream_url,
                                             instance.role,
                                             send_otp
                                             )
        elif instance.role == "viewer":
            send_mail_invite = attendee_mail(instance.name,
                                             instance.email,
                                             instance.cast.event_name,
                                             schedule_time,
                                             meeting_url,
                                             v_password,
                                             stream_url,
                                             instance.role,
                                             send_otp
                                             )
        else:
            send_mail_invite = attendee_mail(instance.name,
                                             instance.email,
                                             instance.cast.event_name,
                                             schedule_time,
                                             meeting_url,
                                             m_password,
                                             stream_url,
                                             instance.role,
                                             send_otp
                                             )

