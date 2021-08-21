from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from library.helper import user_info
from rest_framework.status import HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta


class join_meeting(APIView):
    def post(self, request):
        name = request.data['name']
        public_meeting_id = request.data['public_meeting_id']
        password = request.data['password']
        # room_type = request.data['room_type']
        avatar_url = request.data['avatar_url']
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
                result = Meeting.join_url(private_meeting_id,
                                          name,
                                          meeting_obj.moderator_password,
                                          avatar_url
                                          )
                return Response({'status': True,
                                 'url': result}
                                )

            if password == meeting_obj.moderator_password:
                result = Meeting.join_url(private_meeting_id,
                                          name,
                                          meeting_obj.moderator_password,
                                          avatar_url
                                          )
                return Response({'status': True,
                                 'url': result})

            else:  # attendee
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
                sch_time = meeting_obj.schedule_time.time()
                duration = meeting_obj.duration
                reach_time = time_adder(sch_time, duration)
                current = datetime.utcnow().time()
                status = time_in_range(sch_time, reach_time, current)
                if status == True:
                    event_scheduler(private_meeting_id)
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              meeting_obj.moderator_password,
                                              avatar_url)
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


def time_adder(b, duration):
    s2 = '{}:{}:{}'.format(b.hour, b.minute, b.second)
    format = '%H:%M:%S'
    durarion_add = datetime.strptime(s2, format)  + timedelta(minutes=duration)
    duration_added = durarion_add.time()
    added_time = datetime.strptime(str(duration_added), format)  + timedelta(minutes=30)
    return added_time.time()


def time_in_range(start, end, current):

    return start <= current <= end