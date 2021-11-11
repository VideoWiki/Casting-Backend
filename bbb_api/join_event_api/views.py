import json

from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from library.helper import user_info
from rest_framework.status import HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta
import requests

class join_meeting(APIView):
    def post(self, request):
        name = request.data['name']
        public_meeting_id = request.data['public_meeting_id']
        password = request.data['password']
        # room_type = request.data['room_type']
        avatar_url = request.data['avatar_url']
        # avatar_url = ""
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
                event_scheduler(private_meeting_id)
                result = Meeting.join_url(private_meeting_id,
                                          name,
                                          meeting_obj.moderator_password,
                                          avatar_url
                                          )
                return Response({'status': True,
                                 'url': result}
                                )

            if password == meeting_obj.moderator_password:
                status = Meeting.is_meeting_running(private_meeting_id)
                if status == "false":
                    return Response({
                        "status": False,
                        "message": "the event you are trying to join has either ended or yet to begin"
                    },status=HTTP_400_BAD_REQUEST)
                result = Meeting.join_url(private_meeting_id,
                                          name,
                                          meeting_obj.moderator_password,
                                          avatar_url
                                          )
                return Response({'status': True,
                                 'url': result})

            else:  # attendee
                status = Meeting.is_meeting_running(private_meeting_id)
                print(status)
                if status == "false":
                    return Response({
                        "status": False,
                        "message": "the event you are trying to join has either ended or yet to begin"
                    },status=HTTP_400_BAD_REQUEST)
                result = Meeting.join_url(private_meeting_id,
                                          name,
                                          meeting_obj.attendee_password,
                                          avatar_url
                                          )
                return Response({'status': True,
                                 'url': result}
                                )

        else: # meeting is private. password will come
            attendee_password = meeting_obj.attendee_password
            mod_password = meeting_obj.moderator_password
            meeting_user_id = meeting_obj.user_id
            curr_user_id = -1
            try:
                token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
                curr_user_id = user_info(token)
            except:
                pass
            if curr_user_id == meeting_user_id:
                duration = meeting_obj.duration
                if duration == 0:
                    duration = 1440
                subtracted_time = sub_time(meeting_obj.schedule_time)
                added_time = add_time(meeting_obj.schedule_time, duration)
                current = datetime.utcnow()
                status = time_in_range(subtracted_time, added_time, current)
                if status == True:
                    event_scheduler(private_meeting_id)
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              meeting_obj.moderator_password,
                                              avatar_url)
                    if meeting_obj.is_streaming == True:
                        if meeting_obj.bbb_stream_url_youtube != None and meeting_obj.bbb_stream_url_youtube != "":
                            s_url = meeting_obj.bbb_stream_url_youtube
                        else:
                            s_url = meeting_obj.bbb_stream_url_vw
                        if s_url == None:
                            return Response({'status': True,
                                             'url': result}
                                            )
                        url_status = "https://api.stream.video.wiki/api/cast/live/status"
                        payload = {'meeting_id': str(private_meeting_id)}
                        files = []
                        headers = {}
                        response1 = requests.request("POST", url_status, headers=headers, data=payload, files=files)
                        sp = response1.text.split(":")
                        sp2 = sp[1].split(",")
                        if sp2[0] == 'true':
                            url = "https://api.stream.video.wiki/api/cast/live/end"
                            payload = {'meeting_id': '{}'.format(private_meeting_id)}
                            files = []
                            headers = {}
                            response2 = requests.request("POST", url, headers=headers, data=payload, files=files)
                        stream_dict = {
                            "TZ": "Europe/Vienna",
                            "BBB_RESOLUTION": str(meeting_obj.bbb_resolution),
                            "BBB_START_MEETING": "false",
                            "BBB_MEETING_ID": str(meeting_obj.private_meeting_id),
                            "BBB_STREAM_URL": str(s_url),
                            "BBB_SHOW_CHAT": "false",
                            "BBB_USER_NAME": "Live",
                            "BBB_MODERATOR_PASSWORD": str(meeting_obj.moderator_password),
                            "BBB_CHAT_MESSAGE": "Welcome to the stream"
                        }
                        url = "https://api.stream.video.wiki/api/cast/live/start"
                        headers = {
                            'Content-Type': 'application/json'
                        }
                        r = requests.post(url, data=json.dumps(stream_dict), headers= headers)
                    return Response({'status': True,
                                     'url': result}
                                    )
                else:
                    return Response({"status": False,
                                     "message": "please check the scheduled cast start time"},
                                    status=HTTP_400_BAD_REQUEST
                                    )
            elif password == attendee_password:
                try:
                    status = Meeting.is_meeting_running(private_meeting_id)
                    if status == "false":
                        raise "the event you are trying to join has either ended or yet to begin"
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              password,
                                              avatar_url
                                              )
                    return Response({'status': True,
                                     'url': result}
                                    )
                except:
                    message = "the event you are trying to join has either ended or yet to begin"
                    return  Response({'status': False,
                                      'message': message},
                                     status=HTTP_400_BAD_REQUEST
                                     )
            elif password == mod_password:
                try:
                    status = Meeting.is_meeting_running(private_meeting_id)
                    if status == "false":
                        raise "the event you are trying to join has either ended or yet to begin"
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              password,
                                              avatar_url
                                              )
                    return Response({'status': True,
                                     'url': result}
                                    )
                except:
                    message = "the event you are trying to join has either ended or yet to begin"
                    return  Response({'status': False,
                                      'message': message},
                                     status=HTTP_400_BAD_REQUEST
                                     )

            else:
                return Response({'status': False,
                                 'url':None,
                                 'message': 'User validation error'},
                                status=HTTP_400_BAD_REQUEST)

def event_scheduler(private_meeting_id):
    meeting_object = Meeting.objects.get(private_meeting_id=private_meeting_id)
    meeting_object.start()
    return 'created'


def time_in_range(start, end, current):

    return start <= current <= end

def sub_time(b):
    original_time = datetime(year=int(b.year), month=int(b.month), day=int(b.day)) + timedelta(hours=int(b.hour),
                                                                                       minutes=int(b.minute))
    durarion_sub = original_time - timedelta(minutes=30)
    return durarion_sub

def add_time(b, duration):
    original_time = datetime(year=int(b.year), month=int(b.month), day=int(b.day)) + timedelta(hours=int(b.hour),
                                                                                               minutes=int(b.minute))
    durarion_sub = original_time + timedelta(minutes=duration) + timedelta(minutes=30)
    return durarion_sub

def og_time(b):
    original_time = datetime(year=int(b.year), month=int(b.month), day=int(b.day)) + timedelta(hours=int(b.hour),
                                                                                               minutes=int(b.minute))
    return original_time


