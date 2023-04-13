from django.db.models.signals import post_save
from django.dispatch import receiver
from bbb_api.models import Meeting
from bbb_api.create_event_email_sender import event_registration_mail, time_subtractor
from django_q.tasks import schedule
from api.global_variable import CLIENT_DOMAIN_URL, VW_RTMP_URL
from django_q.models import Schedule
from datetime import timedelta


@receiver(post_save, sender=Meeting)
def post_save_prediction(sender, instance, created, update_fields, **kwargs):
    if created:
        creator_email = instance.event_creator_email
        if creator_email == "":
            pass
        else:
            name = instance.event_name
            date = instance.schedule_time.date()
            hour = instance.schedule_time.hour
            min = instance.schedule_time.minute
            schedule_time = str(hour) + ":"+ str(min)
            pre_reg_form_url = f"{CLIENT_DOMAIN_URL}/event-registration/{instance.public_meeting_id}/"
            event_registration_mail(str(creator_email), str(name), str(date), str(schedule_time),
                                    pre_reg_form_url)


    elif update_fields:
        pass
    else:
        creator_email = instance.event_creator_email
        name = instance.event_name
        date = instance.schedule_time.date()
        hour = instance.schedule_time.hour
        min = instance.schedule_time.minute
        schedule_time = str(hour) + ":" + str(min)
        pre_reg_form_url = f"{CLIENT_DOMAIN_URL}/event-registration/{instance.public_meeting_id}/"

        event_registration_mail(str(creator_email), str(name), str(date), str(schedule_time),
                                pre_reg_form_url)


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







