from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from django_q.tasks import schedule
from django_q.models import Schedule
from ..create_event_email_sender import event_registration_mail, \
    time_subtractor, attendee_mail
from api.global_variable import PRO_URL
from library.helper import private_meeting_id_generator, \
    public_meeting_id_generator, user_info, \
    user_info_email, generate_random_key, \
    user_info_name
class create_event(APIView):
    def post(self, request):
        meeting = Meeting()
        name = request.data['event_name']
        if Meeting.objects.filter(event_name__iexact=name):
            return Response({"status": False, "message": "event with this name is already present"})
        else:
            meeting.event_name = name
        meeting.private_meeting_id = private_meeting_id_generator()
        meeting.public_meeting_id = public_meeting_id_generator()
        print(meeting.public_meeting_id,'public meeting id')

        meeting.meeting_type = request.data['meeting_type']
        if meeting.meeting_type == "":
            meeting.meeting_type = "private"
        attendee_password = request.data['attendee_password']

        if attendee_password == '':
            random_password = generate_random_key()
            meeting.attendee_password = random_password
        else:
            meeting.attendee_password = attendee_password

        mod_password = request.data['moderator_password']

        if mod_password == '':
            random_password = generate_random_key()
            meeting.moderator_password = random_password
        else:
            meeting.moderator_password = mod_password

        meeting.max_participant = request.data['max_participant']
        meeting.welcome = request.data['welcome_text']
        meeting.description = request.data['description']
        meeting.short_description = request.data['short_description']
        meeting.record = request.data['record']
        meeting.duration = request.data['duration']
        meeting.logout_url = request.data['logout_url']
        meeting.mute_on_start = request.data['mute_on_start']
        meeting.banner_text = request.data['banner_text']
        # meeting.banner_color = request.data['banner_color']
        meeting.logo = request.data['logo']
        meeting.end_when_no_moderator = request.data['end_when_no_moderator']
        meeting.guest_policy = request.data['guest_policy']
        meeting.allow_moderator_to_unmute_user = request.data['allow_moderator_to_unmute_user']
        meeting.webcam_only_for_moderator = request.data['webcam_only_for_moderator']
        meeting.auto_start_recording = request.data['auto_start_recording']
        meeting.allow_start_stop_recording = request.data['allow_start_stop_recording']
        meeting.disable_cam = request.data['disable_cam']
        meeting.disable_mic = request.data['disable_mic']
        meeting.disable_note = True
        meeting.disable_public_chat = True
        meeting.disable_private_chat = True
        meeting.lock_layout = request.data['lock_layout']
        meeting.lock_on_join = request.data['lock_on_join']
        meeting.hide_users = request.data['hide_users']
        meeting.schedule_time = request.data['schedule_time']
        meeting.moderators = request.data['moderator_emails']
        meeting.primary_color = request.data['primary_color']
        meeting.secondary_color = request.data['secondary_color']
        meeting.back_image = request.data['back_image']
        meeting.event_tag = request.data['event_tag']

        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_id = user_info(str(token))
        if user_id == -1:
            return Response({'status': True, 'message': 'User validation error'})
        meeting.user_id = user_id
        # meeting.save()
        user_name = user_info_name(token)
        if user_id == -1:
            return Response({'status': True, 'message': 'User validation error'})
        meeting.event_creator_name = user_name
        schedular_name = meeting.private_meeting_id
        meeting.schedular_name = schedular_name
        remind_schedular = meeting.public_meeting_id
        meeting.schedular_name_reminder = remind_schedular
        schedule('bbb_api.create_event_api.views.event_scheduler',
                 meeting.private_meeting_id,
                 repeats=-1,
                 schedule_type=Schedule.ONCE,
                 name=schedular_name,
                 next_run= ('{}-{}-{} {}:{}:00'.format(
                     meeting.schedule_time[0:4],
                     meeting.schedule_time[5:7],
                     meeting.schedule_time[8:10],
                     meeting.schedule_time[11:13],
                     meeting.schedule_time[14:16]
                 )))
        m_list = meeting.moderators
        print(type(m_list), len(m_list))
        for email in m_list:
            meeting_url = PRO_URL + "/join={}/".format(meeting.public_meeting_id)
            attendee_password = meeting.attendee_password
            send_mail_invite = attendee_mail(email, meeting.event_name, meeting.schedule_time, meeting_url, attendee_password)

        user_email = user_info_email(token)
        send_mail_registration = event_registration_mail(user_email, meeting.event_name, meeting.schedule_time)
        meeting.event_creator_email = user_email
        meeting.save()
        reminder_time = meeting.schedule_time
        subtracted_time = time_subtractor(reminder_time)
        subtracted_time_final = str(subtracted_time)
        a = subtracted_time_final.split(":")
        if len(a[0]) == 1:
            a[0] = "0"+a[0]
        if len(subtracted_time_final[0:2]) == 1:
            subtracted_time_final[0:2] = "0"+str(subtracted_time_final[0:2])
            print(subtracted_time_final[0:2],"895")
        schedule('bbb_api.create_event_email_sender.event_reminder_mail',
                 user_email, meeting.event_name, meeting.schedule_time,
                 schedule_type=Schedule.ONCE,
                 name=remind_schedular,
                 next_run=('{}-{}-{} {}:{}:00'.format(
                     reminder_time[0:4],
                     reminder_time[5:7],
                     reminder_time[8:10],
                     a[0],
                     a[1]
                 )))
        msg = 'meeting scheduled successfully'
        return Response({'status': True, 'event_name': meeting.event_name,'meeting_id': meeting.public_meeting_id, 'event_tag': meeting.event_tag, 'message': msg})


def event_scheduler(private_meeting_id):
    meeting_object = Meeting.objects.get(private_meeting_id=private_meeting_id)
    meeting_object.start()
    return 'created'