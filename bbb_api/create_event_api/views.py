from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from django_q.tasks import schedule
from django_q.models import Schedule
from ..create_event_email_sender import event_registration_mail, \
    time_subtractor, attendee_mail, time_subtractor2
from api.global_variable import CLIENT_DOMAIN_URL
from library.helper import private_meeting_id_generator, \
    public_meeting_id_generator, user_info, \
    user_info_email, generate_random_key, \
    user_info_name
from rest_framework import status
from .cover_image import cover_image_uploader


class create_event(APIView):
    def post(self, request):
        meeting = Meeting()
        name = request.data['event_name']
        if Meeting.objects.filter(event_name__iexact=name):
            return Response({
                "status": False,
                "message": "event with this name is already present"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            meeting.event_name = name
        meeting.private_meeting_id = private_meeting_id_generator()
        meeting.public_meeting_id = public_meeting_id_generator()
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
        record = request.data['record']
        if record == "":
            record = False
            meeting.record = record
        duration = request.data['duration']
        if duration == "":
            duration = 0
            meeting.duration = duration
        logout_url = request.data['logout_url']
        if logout_url == "":
            logout_url = "https://video.wiki/"
            meeting.logout_url = logout_url
        mute_on_start = request.data['mute_on_start']
        if mute_on_start == "":
            mute_on_start = False
            meeting.mute_on_start = mute_on_start
        banner_text = request.data['banner_text']
        if banner_text == "":
            banner_text = "Welcome to the Cast"
            meeting.banner_text = banner_text
        # meeting.banner_color = request.data['banner_color']
        meeting.logo = request.data['logo']
        end_when_no_moderator = request.data['end_when_no_moderator']
        if end_when_no_moderator =="":
            end_when_no_moderator = True
            meeting.end_when_no_moderator = end_when_no_moderator
        guest_policy = request.data['guest_policy']
        if guest_policy == "":
            guest_policy = "ALWAYS_ACCEPT"
            meeting.guest_policy = guest_policy
        allow_moderator_to_unmute_user = request.data['allow_moderator_to_unmute_user']
        if allow_moderator_to_unmute_user == "":
            allow_moderator_to_unmute_user = True
            meeting.allow_moderator_to_unmute_user = allow_moderator_to_unmute_user
        webcam_only_for_moderator = request.data['webcam_only_for_moderator']
        if webcam_only_for_moderator == "":
            webcam_only_for_moderator = True
            meeting.webcam_only_for_moderator = webcam_only_for_moderator
        auto_start_recording = request.data['auto_start_recording']
        if auto_start_recording == "":
            auto_start_recording = True
            meeting.auto_start_recording = auto_start_recording
        allow_start_stop_recording = request.data['allow_start_stop_recording']
        if allow_start_stop_recording == "":
            allow_start_stop_recording =  True
            meeting.allow_start_stop_recording = allow_start_stop_recording
        disable_cam = request.data['disable_cam']
        if disable_cam == "":
            disable_cam = True
            meeting.disable_cam = disable_cam
        disable_mic = request.data['disable_mic']
        if disable_mic == "":
            disable_mic = True
            meeting.disable_mic = disable_mic
        meeting.disable_note = True
        meeting.disable_public_chat = True
        meeting.disable_private_chat = True
        lock_layout = request.data['lock_layout']
        if lock_layout == "":
            lock_layout = True
            meeting.lock_layout = lock_layout
        lock_on_join = request.data['lock_on_join']
        if lock_on_join == "":
            lock_on_join = True
            meeting.lock_on_join = lock_on_join
        hide_users = request.data['hide_users']
        if hide_users == "":
            hide_users = True
            meeting.hide_users = hide_users
        schedule_time = request.data['schedule_time']
        if schedule_time == "":
            return Response({"status": False,
                             "message": "no time provided"},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        meeting.schedule_time = schedule_time
        meeting.moderators = request.data['invitee_details']
        meeting.primary_color = request.data['primary_color']
        meeting.secondary_color = request.data['secondary_color']
        meeting.back_image = request.data['back_image']
        meeting.event_tag = request.data['event_tag']
        cover_image = request.data["cover_image"]
        if cover_image != "":
            cover_image_status = cover_image_uploader(cover_image)
            meeting.cover_image = cover_image_status
        else:
            cover_image = "http://s3.us-east-2.amazonaws.com/video.wiki/media/custom_background/PhotobyFranciscoGhisletti.jpg"
            meeting.cover_image = cover_image

        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_id = user_info(str(token))
        if user_id == -1:
            return Response({
                'status': True,
                'message': 'User validation error'},
                status=status.HTTP_400_BAD_REQUEST
            )
        meeting.user_id = user_id
        # meeting.save()
        user_name = user_info_name(token)
        if user_id == -1:
            return Response({
                'status': True,
                'message': 'User validation error'},
                status=status.HTTP_400_BAD_REQUEST)
        meeting.event_creator_name = user_name
        remind_schedular = meeting.public_meeting_id
        meeting.schedular_name_reminder = remind_schedular
        m_list = meeting.moderators
        if len(m_list) != 0:
            for item in m_list:
                meeting_url = CLIENT_DOMAIN_URL + "/e/{}/".format(meeting.public_meeting_id)
                a_password = meeting.attendee_password
                m_password = meeting.moderator_password
                if item["type"] == "speaker":
                    send_mail_invite = attendee_mail(item["name"],
                                                     item["email"],
                                                     meeting.event_name,
                                                     meeting.schedule_time,
                                                     meeting_url,
                                                     m_password
                                                     )

                else:
                    send_mail_invite = attendee_mail(item["name"],
                                                     item["email"],
                                                     meeting.event_name,
                                                     meeting.schedule_time,
                                                     meeting_url,
                                                     a_password
                                                     )

        user_email = user_info_email(token)
        send_mail_registration = event_registration_mail(user_email,
                                                         meeting.event_name,
                                                         meeting.schedule_time
                                                         )
        meeting.event_creator_email = user_email
        meeting.save()
        reminder_time = meeting.schedule_time
        subtracted_time = time_subtractor(reminder_time)
        subtracted_time_final = str(subtracted_time)
        a = subtracted_time_final.split(":")
        if len(a[0]) == 1:
            a[0] = "0" + a[0]
        if len(subtracted_time_final[0:2]) == 1:
            subtracted_time_final[0:2] = "0" + str(subtracted_time_final[0:2])
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
        return Response({'status': True, 'event_name': meeting.event_name,
                         'meeting_id': meeting.public_meeting_id,
                         'tag': meeting.event_tag,
                         'cover_image': meeting.cover_image,
                         'message': msg}
                        )


