from django.db.models.signals import post_save
from django.dispatch import receiver
from bbb_api.models import Meeting
from bbb_api.create_event_email_sender import event_registration_mail, time_subtractor
from django_q.tasks import schedule
from api.global_variable import CLIENT_DOMAIN_URL
from django_q.models import Schedule
from datetime import timedelta


@receiver(post_save, sender=Meeting)
def post_save_prediction(sender, instance, created, update_fields, **kwargs):
    if created:
        creator_email = instance.event_creator_email
        name = instance.event_name
        date = instance.schedule_time.date()
        hour = instance.schedule_time.hour
        min = instance.schedule_time.minute
        print(instance.schedule_time, "st")
        start_time = instance.schedule_time
        schedule_time = str(date) +" at "+ str(hour) + ":"+ str(min) + " GMT"
        vw_stream = instance.bbb_stream_url_vw
        user_name = instance.event_creator_name
        meeting_url = CLIENT_DOMAIN_URL + "/e/{}/".format(instance.public_meeting_id)
        audience_airdrop = instance.audience_airdrop
        if audience_airdrop == True:
            nft_drop_url = CLIENT_DOMAIN_URL + "/nftdrop/?cast_id={}".format(instance.public_meeting_id)
        else:
            nft_drop_url = ""
        if vw_stream == None:
            stream_url = ""
        else:
            stream_url = "{}/live/{}".format(CLIENT_DOMAIN_URL, instance.public_meeting_id)
        send_otp = instance.send_otp
        viewer_mode = instance.viewer_mode
        event_type = instance.meeting_type
        viewer_password = instance.viewer_password
        pre_reg_form_url = f"{CLIENT_DOMAIN_URL}/event-registration/{instance.public_meeting_id}/"
        event_registration_mail(str(creator_email), str(user_name),str(name), str(schedule_time),
                                stream_url, meeting_url, nft_drop_url, instance.moderator_password,
                                instance.attendee_password, send_otp, pre_reg_form_url, start_time,
                                event_type, viewer_mode, viewer_password)
    elif update_fields:
        pass
    else:
        creator_email = instance.event_creator_email
        name = instance.event_name
        start_time = instance.schedule_time
        date = instance.schedule_time.date()
        hour = instance.schedule_time.hour
        min = instance.schedule_time.minute
        schedule_time = str(date) + " at " + str(hour) + ":" + str(min) + " GMT"
        vw_stream = instance.bbb_stream_url_vw
        user_name = instance.event_creator_name
        meeting_url = CLIENT_DOMAIN_URL + "/e/{}/".format(instance.public_meeting_id)
        audience_airdrop = instance.audience_airdrop
        send_otp = instance.send_otp
        if audience_airdrop == True:
            nft_drop_url = CLIENT_DOMAIN_URL + "/nftdrop/?cast_id={}".format(instance.public_meeting_id)
        else:
            nft_drop_url = ""
        if vw_stream == None:
            stream_url = ""
        else:
            stream_url = "{}/live/{}".format(CLIENT_DOMAIN_URL, instance.public_meeting_id)
        pre_reg_form_url = f"{CLIENT_DOMAIN_URL}/event-registration/{instance.public_meeting_id}/"
        event_type = instance.meeting_type
        viewer_mode = instance.viewer_mode
        viewer_password = instance.viewer_password
        event_registration_mail(str(creator_email), str(user_name), str(name), str(schedule_time),
                                stream_url, meeting_url, nft_drop_url, instance.moderator_password,
                                instance.attendee_password, send_otp, pre_reg_form_url, start_time,
                                event_type, viewer_mode, viewer_password)


@receiver(post_save, sender=Meeting)
def reminder(sender, instance, created, update_fields, **kwargs):
    if created:
        remind_schedular = instance.public_meeting_id
        reminder_time = instance.schedule_time
        reminder_mail_time = reminder_time + timedelta(minutes=-10)

        schedule('bbb_api.create_event_api.helper.email_sender',
                 instance.public_meeting_id,
                 schedule_type=Schedule.ONCE,
                 name=remind_schedular,
                 next_run= reminder_mail_time)


    elif update_fields:
        pass
    else:
        remind_schedular = instance.public_meeting_id
        try:
            get_remind_object = Schedule.objects.get(name__iexact=remind_schedular)
            get_remind_object.delete()
        except:
            pass
        reminder_time = instance.schedule_time
        reminder_mail_time = reminder_time + timedelta(minutes=-10)
        schedule('bbb_api.create_event_api.helper.email_sender',
                 instance.public_meeting_id,
                 schedule_type=Schedule.ONCE,
                 name=remind_schedular,
                 next_run=reminder_mail_time)




