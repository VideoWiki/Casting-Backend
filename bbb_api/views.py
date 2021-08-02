from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
import uuid
from .models import Meeting
from rest_framework.response import Response
from django_q.tasks import schedule
from django_q.models import Schedule
from rest_framework_simplejwt.backends import TokenBackend
from django.utils.crypto import get_random_string


def generate_random_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(8, chars)

    return secret_key

def meeeting_id_generator():
    id = str(uuid.uuid4())
    return id


class create_event(APIView):
    def post(self, request):
        meeting = Meeting()
        meeting.name = request.data['name']
        meeting.meeting_id = meeeting_id_generator()
        meeting.meeting_type = request.data['meeting_type']
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


        meeting.welcome = request.data['welcome_text']
        meeting.record = request.data['record']
        meeting.duration = request.data['duration']
        meeting.logout_url = request.data['logout_url']
        meeting.mute_on_start = request.data['mute_on_start']
        meeting.banner_text = request.data['banner_text']
        meeting.copyright = request.data['copyright']
        meeting.moderator_only_message = request.data['moderator_only_message']
        meeting.logo = request.data['logo']
        meeting.end_when_no_moderator = request.data['end_when_no_moderator']
        meeting.guest_policy = request.data['guest_policy']
        meeting.allow_moderator_to_unmute_user = request.data['allow_moderator_to_unmute_user']
        meeting.webcam_only_for_moderator = request.data['webcam_only_for_moderator']
        meeting.auto_start_recording = request.data['auto_start_recording']
        meeting.allow_start_stop_recording = request.data['allow_start_stop_recording']
        meeting.disable_cam = request.data['disable_cam']
        meeting.disable_mic = request.data['disable_mic']
        meeting.disable_note = request.data['disable_note']
        meeting.disable_public_chat = request.data['disable_public_chat']
        meeting.disable_private_chat = request.data['disable_private_chat']
        meeting.lock_layout = request.data['lock_layout']
        meeting.lock_on_join = request.data['lock_on_join']
        meeting.hide_users = request.data['hide_users']
        meeting.schedule_time = request.data['schedule_time']

        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_id = user_info(str(token))
        if user_id == -1:
            return Response({'status': True, 'message': 'User validation error'})
        meeting.user_id = user_id
        meeting.save()
        schedule('bbb_api.views.event_scheduler',
                 meeting.meeting_id,
                 repeats=-1,
                 schedule_type=Schedule.ONCE,
                 next_run= ('{}-{}-{} {}:{}:00'.format(
                     meeting.schedule_time[0:4],
                     meeting.schedule_time[5:7],
                     meeting.schedule_time[8:10],
                     meeting.schedule_time[11:13],
                     meeting.schedule_time[14:16]
                 )))
        msg = 'meeting scheduled successfully'
        return Response({'status': True, 'meeting_id': meeting.meeting_id, 'message': msg})



class join_meeting(APIView):
    def post(self, request):
        name = request.data['name']
        meeting_id = request.data['meeting_id']
        password = request.data['password']
        room_type = request.data['room_type']
        avatar_url = request.data['avatar_url']
        guest = request.data['guest']
        skip_check_audio = request.data['skip_check_audio']
        skip_check_audio_on_first_join = request.data['skip_check_audio_on_first_join']
        meeting_obj = Meeting.objects.get(meeting_id=meeting_id)
        meeting_type = meeting_obj.meeting_type

        if meeting_type == 'public':

            meeting_user_id = meeting_obj.user_id
            curr_user_id = -1
            try:
                token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
                curr_user_id = user_info(token)
            except:
                pass

            if curr_user_id == meeting_user_id:
                result = Meeting.join_url(meeting_id, name, meeting_obj.moderator_password, avatar_url, guest, skip_check_audio,
                                          skip_check_audio_on_first_join)
                return Response({'status': True, 'url': result})
            else:  # attendee
                result = Meeting.join_url(meeting_id, name, meeting_obj.attendee_password, avatar_url, guest, skip_check_audio,
                                          skip_check_audio_on_first_join)
                return Response({'status': True, 'url': result})

        else: # meeting is private. password will come
            attendee_password = meeting_obj.attendee_password
            mod_password = meeting_obj.moderator_password
            if password == attendee_password:
                result = Meeting.join_url(meeting_id, name, password, avatar_url, guest, skip_check_audio,
                                          skip_check_audio_on_first_join)
                return Response({'status': True, 'url': result})

            elif password == mod_password:
                result = Meeting.join_url(meeting_id, name, password, avatar_url, guest, skip_check_audio,
                                          skip_check_audio_on_first_join)
                return Response({'status': True, 'url': result})

            else:
                return Response({'status': False, 'url':None, 'message': 'User validation error'})



class delete_meeting(APIView):
    def post(self, request):
        meeting_id = request.data['meeting_id']
        password = request.data['password']
        try:
            result = Meeting.end_meeting(meeting_id, password)
            return Response({'status': True, 'message': 'meeting deleted successfully'})
        except:
            return Response({'status': False, 'message': 'Unable to end meeting'})


class meetings(APIView):
    def get(self, request):
        meetings = Meeting.get_meetings()
        return Response({'status': True, 'meetings': meetings})

class is_meeting_running(APIView):
    def post(self, request):
        meeting_id = request.data['meeting_id']
        result = Meeting.is_meeting_running(meeting_id)
        return Response({'status': True, 'meeting_running': result})

class meeting_info(APIView):
    def post(self, request):
        meeting_id = request.data['meeting_id']
        password = request.data['password']
        result = Meeting.meeting_info(meeting_id, password)
        return Response({'status': True, 'meeting_info': result})


def event_scheduler(meeting_id):
    meeting_object = Meeting.objects.get(meeting_id=meeting_id)
    meeting_object.start()
    return 'created'

def user_info(token):

        data = {'token': token}
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user_id = valid_data['user_id']
            return user_id

        except ValidationError as v:
            return -1

