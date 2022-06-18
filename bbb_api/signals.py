from django.db.models.signals import post_save
from django.dispatch import receiver
from bbb_api.models import Meeting
from bbb_api.create_event_email_sender import event_registration_mail, time_subtractor
from django_q.tasks import schedule
from api.global_variable import CLIENT_DOMAIN_URL
from django_q.models import Schedule


@receiver(post_save, sender=Meeting)
def post_save_prediction(sender, instance, created, update_fields, **kwargs):
    if created:
        creator_email = instance.event_creator_email
        name = instance.event_name
        date = instance.schedule_time.date()
        hour = instance.schedule_time.hour
        min = instance.schedule_time.minute
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
        event_registration_mail(str(creator_email), str(user_name),str(name), str(schedule_time),
                                stream_url, meeting_url, nft_drop_url, instance.moderator_password, instance.attendee_password)
    elif update_fields:
        pass
    else:
        creator_email = instance.event_creator_email
        name = instance.event_name
        date = instance.schedule_time.date()
        hour = instance.schedule_time.hour
        min = instance.schedule_time.minute
        schedule_time = str(date) + " at " + str(hour) + ":" + str(min) + " GMT"
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
        event_registration_mail(str(creator_email), str(user_name), str(name), str(schedule_time),
                                stream_url, meeting_url, nft_drop_url, instance.moderator_password, instance.attendee_password)


# @receiver(post_save, sender=Meeting)
# def emailer(sender, instance, created, **kwargs):
#     if created:
#         m_list = instance.moderators
#         e_list = []
#         for i in m_list:
#             email = i["email"]
#             e_list.append(email)
#         if len(m_list) != 0:
#             for item in m_list:
#                 meeting_url = CLIENT_DOMAIN_URL + "/e/{}/".format(instance.public_meeting_id)
#                 a_password = instance.attendee_password
#                 m_password = instance.moderator_password
#                 vw_stream = instance.bbb_stream_url_vw
#                 if vw_stream == None:
#                     stream_url = ""
#                 else:
#                     stream_url = "https://play.stream.video.wiki/live/{}".format(instance.public_meeting_id)
#                 if item["type"] == "speaker":
#                     send_mail_invite = attendee_mail(item["name"],
#                                                      item["email"],
#                                                      instance.event_name,
#                                                      instance.schedule_time,
#                                                      meeting_url,
#                                                      m_password,
#                                                      stream_url
#                                                      )
#
#                 else:
#                     send_mail_invite = attendee_mail(item["name"],
#                                                      item["email"],
#                                                      instance.event_name,
#                                                      instance.schedule_time,
#                                                      meeting_url,
#                                                      a_password,
#                                                      stream_url
#                                                      )
#
#
@receiver(post_save, sender=Meeting)
def reminder(sender, instance, created, update_fields, **kwargs):
    if created:
        remind_schedular = instance.public_meeting_id
        reminder_time = instance.schedule_time
        subtracted_time = time_subtractor(reminder_time)
        subtracted_time_final = str(subtracted_time)
        a = subtracted_time_final.split(":")
        if len(a[0]) == 1:
            a[0] = "0" + a[0]
        if len(subtracted_time_final[0:2]) == 1:
            subtracted_time_final[0:2] = "0" + str(subtracted_time_final[0:2])
        schedule('bbb_api.create_event_api.helper.email_sender',
                 instance.public_meeting_id,
                 schedule_type=Schedule.ONCE,
                 name=remind_schedular,
                 next_run=('{}-{}-{} {}:{}:00'.format(
                     reminder_time.year,
                     reminder_time.month,
                     reminder_time.day,
                     a[0],
                     a[1]
                 )))
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
        subtracted_time = time_subtractor(reminder_time)
        subtracted_time_final = str(subtracted_time)
        a = subtracted_time_final.split(":")
        if len(a[0]) == 1:
            a[0] = "0" + a[0]
        if len(subtracted_time_final[0:2]) == 1:
            subtracted_time_final[0:2] = "0" + str(subtracted_time_final[0:2])
        schedule('bbb_api.create_event_api.helper.email_sender',
                 instance.public_meeting_id,
                 schedule_type=Schedule.ONCE,
                 name=remind_schedular,
                 next_run=('{}-{}-{} {}:{}:00'.format(
                     reminder_time.year,
                     reminder_time.month,
                     reminder_time.day,
                     a[0],
                     a[1]
                 )))




