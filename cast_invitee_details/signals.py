from .models import CastInviteeDetails
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.global_variable import CLIENT_DOMAIN_URL
from bbb_api.create_event_email_sender import attendee_mail
from bbb_api.models import Meeting
@receiver(post_save, sender=CastInviteeDetails)
def post_save_emailer(sender, instance, created, **kwargs):

    if created:
        print(instance.cast.event_name, instance.role, instance.email)
        meeting_url = CLIENT_DOMAIN_URL + "/e/{}/".format(instance.cast.public_meeting_id)
        cast_id = instance.cast.public_meeting_id
        a_password = instance.cast.attendee_password
        m_password = instance.cast.moderator_password
        v_password = instance.cast.viewer_password
        vw_stream = instance.cast.bbb_stream_url_vw
        cast_type = Meeting.objects.get(public_meeting_id=instance.cast.public_meeting_id).meeting_type
        dt = instance.cast.schedule_time
        date = dt.date()
        hour = dt.hour
        min = dt.minute
        schedule_time = str(hour) + ":" + str(min)
        send_otp = instance.cast.send_otp
        creator_email = instance.cast.event_creator_email
        creator_name = instance.cast.event_creator_name
        viewer_mode = instance.cast.viewer_mode
        public_otp = instance.cast.public_otp
        description = instance.cast.description
        if vw_stream == None:
            stream_url = ""
        else:
            stream_url = "{}/live/{}".format(CLIENT_DOMAIN_URL,instance.cast.public_meeting_id)
        attendee_mail(instance.email,
                      instance.cast.event_name,
                      schedule_time,
                      meeting_url,
                      a_password,
                      m_password,
                      stream_url,
                      instance.role,
                      send_otp,
                      cast_type,
                      dt,
                      creator_email,
                      creator_name,
                      viewer_mode,
                      public_otp,
                      v_password,
                      cast_id,
                      date,
                      description
                      )

