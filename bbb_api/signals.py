from django.db.models.signals import post_save
from django.dispatch import receiver
from bbb_api.models import Meeting
from bbb_api.create_event_email_sender import event_registration_mail, time_subtractor
from django_q.tasks import schedule
from django_q.models import Schedule


@receiver(post_save, sender=Meeting)
def post_save_prediction(sender, instance, created, **kwargs):

    if created:
        creator_email = instance.event_creator_email
        name = instance.event_name
        schedule_time = instance.schedule_time
        vw_stream = instance.bbb_stream_url_vw
        user_name = instance.event_creator_name
        if vw_stream == None:
            stream_url = ""
        else:
            stream_url = "https://play.stream.video.wiki/live/{}".format(instance.public_meeting_id)
        event_registration_mail(str(creator_email), str(user_name),str(name), str(schedule_time), stream_url)



@receiver(post_save, sender=Meeting)
def reminder(sender, instance, created, **kwargs):
    if created:
        remind_schedular = instance.public_meeting_id
        reminder_time = instance.schedule_time
        subtracted_time = time_subtractor(reminder_time)
        subtracted_time_final = str(subtracted_time)
        print(subtracted_time_final, "here")
        a = subtracted_time_final.split(":")
        if len(a[0]) == 1:
            a[0] = "0" + a[0]
        if len(subtracted_time_final[0:2]) == 1:
            subtracted_time_final[0:2] = "0" + str(subtracted_time_final[0:2])
        print(a[0], a[1])
        schedule('bbb_api.create_event_api.helper.email_sender',
                 instance.event_name,
                 schedule_type=Schedule.ONCE,
                 name=remind_schedular,
                 next_run=('{}-{}-{} {}:{}:00'.format(
                     reminder_time.year,
                     reminder_time.month,
                     reminder_time.day,
                     a[0],
                     a[1]
                 )))




