from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
import uuid
from .models import Meeting
from rest_framework.response import Response
from django_q.tasks import schedule
from django_q.models import Schedule
from rest_framework_simplejwt.backends import TokenBackend
from django.utils.crypto import get_random_string
from .create_event_email_sender import event_registration_mail, time_subtractor, attendee_mail
from api.global_variable import PRO_URL
from django.core.exceptions import ObjectDoesNotExist
import django.utils.timezone


def generate_random_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(8, chars)

    return secret_key

def private_meeting_id_generator():
    id = str(uuid.uuid4())
    return id

def public_meeting_id_generator():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    public_meeting_id = get_random_string(3, chars) + '-' + get_random_string(3, chars) + '-' + get_random_string(3, chars)
    return public_meeting_id

class create_event(APIView):
    def post(self, request):
        meeting = Meeting()
        meeting.name = request.data['name']
        meeting.private_meeting_id = private_meeting_id_generator()
        meeting.public_meeting_id = public_meeting_id_generator()
        print(meeting.public_meeting_id,'public meeting id')

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
        meeting.moderators = request.data['moderator_emails']
        print(meeting.moderators)
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_id = user_info(str(token))
        if user_id == -1:
            return Response({'status': True, 'message': 'User validation error'})
        meeting.user_id = user_id
        meeting.save()
        schedule('bbb_api.views.event_scheduler',
                 meeting.private_meeting_id,
                 repeats=-1,
                 schedule_type=Schedule.ONCE,
                 next_run= ('{}-{}-{} {}:{}:00'.format(
                     meeting.schedule_time[0:4],
                     meeting.schedule_time[5:7],
                     meeting.schedule_time[8:10],
                     meeting.schedule_time[11:13],
                     meeting.schedule_time[14:16]
                 )))
        m_list = meeting.moderators
        print(m_list,";;;")
        for email in m_list:
            meeting_url = PRO_URL + "/join={}/".format(meeting.public_meeting_id)
            attendee_password = meeting.attendee_password
            send_mail = attendee_mail(email, meeting.name, meeting.schedule_time, meeting_url, attendee_password)

        user_email = user_info_email(token)
        send_mail = event_registration_mail(user_email, meeting.name, meeting.schedule_time)
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
                 user_email, meeting.name, meeting.schedule_time,
                 schedule_type=Schedule.ONCE,
                 next_run=('{}-{}-{} {}:{}:00'.format(
                     reminder_time[0:4],
                     reminder_time[5:7],
                     reminder_time[8:10],
                     a[0],
                     a[1]
                 )))
        msg = 'meeting scheduled successfully'
        return Response({'status': True, 'meeting_id': meeting.public_meeting_id, 'message': msg})



class join_meeting(APIView):
    def post(self, request):
        name = request.data['name']
        public_meeting_id = request.data['public_meeting_id']
        password = request.data['password']
        room_type = request.data['room_type']
        avatar_url = request.data['avatar_url']
        guest = request.data['guest']
        skip_check_audio = request.data['skip_check_audio']
        skip_check_audio_on_first_join = request.data['skip_check_audio_on_first_join']
        meeting_obj = Meeting.objects.get(public_meeting_id=public_meeting_id)
        meeting_type = meeting_obj.meeting_type
        private_meeting_id = meeting_obj.private_meeting_id
        if meeting_type == 'public':

            meeting_user_id = meeting_obj.user_id
            curr_user_id = -1
            try:
                token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
                curr_user_id = user_info(token)
            except:
                pass

            if curr_user_id == meeting_user_id:
                result = Meeting.join_url(private_meeting_id, name, meeting_obj.moderator_password, avatar_url, guest, skip_check_audio,
                                          skip_check_audio_on_first_join)
                return Response({'status': True, 'url': result})

            if password == meeting_obj.moderator_password:
                result = Meeting.join_url(private_meeting_id, name, meeting_obj.moderator_password, avatar_url, guest, skip_check_audio,
                                          skip_check_audio_on_first_join)
                return Response({'status': True, 'url': result})

            else:  # attendee
                result = Meeting.join_url(private_meeting_id, name, meeting_obj.attendee_password, avatar_url, guest, skip_check_audio,
                                          skip_check_audio_on_first_join)
                return Response({'status': True, 'url': result})

        else: # meeting is private. password will come
            attendee_password = meeting_obj.attendee_password
            mod_password = meeting_obj.moderator_password
            if password == attendee_password:
                result = Meeting.join_url(private_meeting_id, name, password, avatar_url, guest, skip_check_audio,
                                          skip_check_audio_on_first_join)
                return Response({'status': True, 'url': result})

            elif password == mod_password:
                result = Meeting.join_url(private_meeting_id, name, password, avatar_url, guest, skip_check_audio,
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
        public_meeting_id = request.data['public_meeting_id']
        private_meeting_id = Meeting.objects.get(public_meeting_id=public_meeting_id)
        result = Meeting.is_running(private_meeting_id)
        return Response({'status': True, 'meeting_running': result})

class meeting_info(APIView):
    def post(self, request):
        meeting_id = request.data['meeting_id']
        password = request.data['password']
        result = Meeting.meeting_info(meeting_id, password)
        return Response({'status': True, 'meeting_info': result})


class get_recordings(APIView):
    def post(self, request):
        meeting_id = request.data['meeting_id']
        private_meeting_id = Meeting.objects.get(public_meeting_id=meeting_id).private_meeting_id
        print(private_meeting_id)
        result = Meeting.get_recordings(private_meeting_id)
        return Response({'status': True, 'recordings': result})


class user_recordings(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_id = user_info(str(token))
        a = Meeting.objects.filter(user_id=user_id)
        b = a.all()
        c = b.filter().values("private_meeting_id")
        d = []
        l = list(c)
        for i in l:
            c = i["private_meeting_id"]
            d.append(c)
        fl = []
        for i in d:
            result = Meeting.get_recordings(i)
            if result!= None:
                fl.append(result)
        return Response({"status": fl})


class scheduled_meetings(APIView):
    def post(self, request):
        meeting = Meeting
        scheduled_meetings = meeting.objects.filter().all().order_by('-schedule_time')
        a = list(scheduled_meetings)
        l = []
        for i in a:
            name = i.name
            day = i.schedule_time.date()
            time = i.schedule_time.time()
            description = i.welcome
            session_key = i.public_meeting_id
            event_id = i.id
            d = {"meeting_name": name, "meeting_day": day,
                 "meeting_time": time, "description": description,
                 "session_key": session_key, "event_id": event_id}
            l.append(d)
        return Response({"status": True, "scheduled_meetings": l})



class meeting_type_checker(APIView):
    def post(self, request):
        session_key = request.data['session_key']
        print(session_key)
        try:
            get_model = Meeting.objects.get(public_meeting_id=session_key)
            type = get_model.meeting_type
        except ObjectDoesNotExist:
            return Response({"status": False, "message": "incorrect session key"})

        if type == "public":
            return Response({"status": True, "event_type": type})
        else:
            return Response({"status": True, "event_type": type})


class my_events(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_id = user_info(str(token))
        user_meetings = Meeting.objects.filter(user_id=user_id).all().order_by('-schedule_time')
        my_event_list = []
        scheduled_event_list = []
        events = Meeting.objects.filter(schedule_time__gt=django.utils.timezone.now())
        for i in events:
            event = i.name
            scheduled_event_list.append(event)
        for i in events:
            private_meeting_id = i.private_meeting_id
            name = i.name
            event = Meeting.is_meeting_running(private_meeting_id=private_meeting_id)
            scheduled_event_list.append(name)
        for event in user_meetings:
            print(scheduled_event_list,"list")
            event_name = event.name
            event_password = event.moderator_password
            event_date = event.schedule_time.date()
            event_time = event.schedule_time.time()
            private_meeting_id = event.private_meeting_id
            event.is_running = Meeting.is_meeting_running(private_meeting_id)
            is_running = event.is_running
            if event.name in scheduled_event_list:
                event_expired = False
            else:
                event_expired = True
            my_event_list.append({"event_name": event_name,
                                  "moderator_password": event_password,
                                  "event_date": event_date,
                                  "event_time": event_time,
                                  "is_running": is_running,
                                  "event_expired": event_expired
                         })
        return Response({"status": True,
                         "my_events": my_event_list
                         })




def event_scheduler(private_meeting_id):
    meeting_object = Meeting.objects.get(private_meeting_id=private_meeting_id)
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


def user_info_email(token):
    data = {'token': token}
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        email = valid_data['email']
        return email

    except ValidationError as v:
        return -1

