import json
from rest_framework.views import APIView
from ..models import Meeting, ViewerDetails
from rest_framework.response import Response
from library.helper import user_info
from rest_framework.status import HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta
import requests
from cast_invitee_details.models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist
from api.global_variable import CLIENT_DOMAIN_URL
import ast


class join_meeting(APIView):
    def post(self, request):
        name = request.data['name']
        public_meeting_id = request.data['public_meeting_id']
        email = request.data["email"]
        password = request.data['password']
        if email != "":
            email = email.lower()

        meeting_obj = Meeting.objects.get(public_meeting_id=str(public_meeting_id))
        meeting_type = meeting_obj.meeting_type
        private_meeting_id = meeting_obj.private_meeting_id
        send_otp = meeting_obj.send_otp
        pub_otp = meeting_obj.public_otp
        viewer_mode = meeting_obj.viewer_mode
        invitee_obj = CastInviteeDetails.objects.filter(cast=meeting_obj)
        join_count = meeting_obj.join_count
        if join_count < 200:
            pass
        else:
            stream_url = "{}/live/{}".format(CLIENT_DOMAIN_URL, public_meeting_id)
            return Response({
                "status": True,
                "stream_url": stream_url,
                "message": "server cap reached. user re-directed to stream"
            })
        if meeting_type == 'public':

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
                name = meeting_obj.event_creator_name
                if status == True:
                    event_scheduler(private_meeting_id)
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              meeting_obj.moderator_password,
                                              force_listen_only=False,
                                              enable_screen_sharing=True,
                                              enable_webcam=True
                                              )
                    meeting_obj.join_count = meeting_obj.join_count + 1
                    meeting_obj.save(update_fields=['join_count'])
                    if meeting_obj.is_streaming == True:
                        stream_urls_list = ast.literal_eval(meeting_obj.bbb_stream_url_vw)
                        if len(stream_urls_list) == 0:
                            pass
                        else:
                            stream_str = ","
                            new_stream_str = stream_str.join(stream_urls_list)
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
                                "BBB_STREAM_URL": new_stream_str,
                                "BBB_SHOW_CHAT": "false",
                                "BBB_USER_NAME": "Live",
                                "BBB_MODERATOR_PASSWORD": str(meeting_obj.moderator_password),
                                "BBB_CHAT_MESSAGE": "Welcome to the stream"
                            }
                            url = "https://api.stream.video.wiki/api/cast/live/start"
                            headers = {
                                'Content-Type': 'application/json'
                            }
                            r = requests.post(url, data=json.dumps(stream_dict), headers=headers)
                    return Response({'status': True,
                                     'url': result}
                                    )
                else:
                    return Response({"status": False,
                                     "message": "please check the scheduled cast start time"},
                                    status=HTTP_400_BAD_REQUEST
                                    )
            status = Meeting.is_meeting_running(private_meeting_id)
            if status == "false":
                message = "the event you are trying to join has either ended or yet to begin"
                return Response({'status': False,
                                 'message': message},
                                status=HTTP_400_BAD_REQUEST
                                )
            else:
                if viewer_mode == False:
                    if password !="":
                        if password == meeting_obj.moderator_password:
                            result = Meeting.join_url(private_meeting_id,
                                                      name,
                                                      meeting_obj.moderator_password,
                                                      force_listen_only=False,
                                                      enable_screen_sharing=True,
                                                      enable_webcam=True
                                                      )
                            meeting_obj.join_count = meeting_obj.join_count + 1
                            meeting_obj.save(update_fields=['join_count'])
                            if email != "":
                                if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                                    joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                                    joinee_obj.joined = True
                                    joinee_obj.save()
                            return Response({'status': True,
                                             'url': result}
                                            )

                        elif password == meeting_obj.attendee_password:
                            result = Meeting.join_url(private_meeting_id,
                                                      name,
                                                      meeting_obj.attendee_password,
                                                      force_listen_only=False,
                                                      enable_screen_sharing=True,
                                                      enable_webcam=True
                                                      )
                            meeting_obj.join_count = meeting_obj.join_count + 1
                            meeting_obj.save(update_fields=['join_count'])
                            if email != "":
                                if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                                    joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                                    joinee_obj.joined = True
                                    joinee_obj.save()
                            return Response({'status': True,
                                             'url': result}
                                            )
                        else:
                            message = "incorrect password"
                            return Response({'status': False,
                                             'message': message},
                                            status=HTTP_400_BAD_REQUEST
                                            )
                    else:
                        result = Meeting.join_url(private_meeting_id,
                                                  name,
                                                  meeting_obj.attendee_password,
                                                  force_listen_only=False,
                                                  enable_screen_sharing=True,
                                                  enable_webcam=True
                                                  )
                        meeting_obj.join_count = meeting_obj.join_count + 1
                        meeting_obj.save(update_fields=['join_count'])
                        if email != "":
                            if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                                joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                                joinee_obj.joined = True
                                joinee_obj.save()
                        return Response({'status': True,
                                         'url': result}
                                        )

                elif viewer_mode == True:
                    if password != "":
                        if password == meeting_obj.moderator_password:
                            result = Meeting.join_url(private_meeting_id,
                                                      name,
                                                      meeting_obj.moderator_password,
                                                      force_listen_only=False,
                                                      enable_screen_sharing=True,
                                                      enable_webcam=True
                                                      )
                            meeting_obj.join_count = meeting_obj.join_count + 1
                            meeting_obj.save(update_fields=['join_count'])
                            if email != "":
                                if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                                    joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                                    joinee_obj.joined = True
                                    joinee_obj.save()
                            return Response({'status': True,
                                             'url': result}
                                            )

                        elif password == meeting_obj.attendee_password:
                            result = Meeting.join_url(private_meeting_id,
                                                      name,
                                                      meeting_obj.attendee_password,
                                                      force_listen_only=False,
                                                      enable_screen_sharing=True,
                                                      enable_webcam=True
                                                      )
                            meeting_obj.join_count = meeting_obj.join_count + 1
                            meeting_obj.save(update_fields=['join_count'])
                            if email != "":
                                if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                                    joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                                    joinee_obj.joined = True
                                    joinee_obj.save()
                            return Response({'status': True,
                                             'url': result}
                                            )
                        else:
                            message = "incorrect password"
                            return Response({'status': False,
                                             'message': message},
                                            status=HTTP_400_BAD_REQUEST
                                            )
                    else:
                        viewer_obj = ViewerDetails.objects.get(cast=meeting_obj)
                        force_listen = viewer_obj.force_listen_only
                        screen_share = viewer_obj.enable_screen_sharing
                        webcam = viewer_obj.enable_webcam
                        result = Meeting.join_url(private_meeting_id,
                                                  name,
                                                  meeting_obj.attendee_password,
                                                  force_listen_only=force_listen,
                                                  enable_screen_sharing=screen_share,
                                                  enable_webcam=webcam
                                                  )
                        meeting_obj.join_count = meeting_obj.join_count + 1
                        meeting_obj.save(update_fields=['join_count'])
                        if email != "":
                            if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                                joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                                joinee_obj.joined = True
                                joinee_obj.save()
                        return Response({'status': True,
                                         'url': result}
                                        )


        else: # meeting is private. password will come
            attendee_password = meeting_obj.attendee_password
            mod_password = meeting_obj.moderator_password
            viewer_password = meeting_obj.viewer_password
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
                name = meeting_obj.event_creator_name
                if status == True:
                    event_scheduler(private_meeting_id)
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              meeting_obj.moderator_password,
                                              force_listen_only=False,
                                              enable_screen_sharing=True,
                                              enable_webcam=True
                                              )
                    meeting_obj.join_count = meeting_obj.join_count + 1
                    meeting_obj.save(update_fields=['join_count'])
                    if meeting_obj.is_streaming == True:
                        stream_urls_list = ast.literal_eval(meeting_obj.bbb_stream_url_vw)
                        if len(stream_urls_list) == 0:
                            pass
                        else:
                            stream_str = ","
                            new_stream_str = stream_str.join(stream_urls_list)
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
                                "BBB_STREAM_URL": new_stream_str,
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

            status = Meeting.is_meeting_running(private_meeting_id)
            if status == "false":
                message = "the event you are trying to join has either ended or yet to begin"
                return Response({'status': False,
                                 'message': message},
                                status=HTTP_400_BAD_REQUEST
                                )
            if meeting_obj.password_auth == True:
                if password == mod_password:
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              meeting_obj.moderator_password,
                                              force_listen_only=False,
                                              enable_screen_sharing=True,
                                              enable_webcam=True
                                              )
                    meeting_obj.join_count = meeting_obj.join_count + 1
                    meeting_obj.save(update_fields=['join_count'])
                    if email != "":
                        if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                            joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                            joinee_obj.joined = True
                            joinee_obj.save()
                    return Response({'status': True,
                                     'url': result}
                                    )

                elif password == meeting_obj.attendee_password:
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              meeting_obj.attendee_password,
                                              force_listen_only=False,
                                              enable_screen_sharing=True,
                                              enable_webcam=True
                                              )
                    meeting_obj.join_count = meeting_obj.join_count + 1
                    meeting_obj.save(update_fields=['join_count'])
                    if email != "":
                        if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                            joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                            joinee_obj.joined = True
                            joinee_obj.save()
                    return Response({'status': True,
                                     'url': result}
                                    )

                elif password == viewer_password:
                    viewer_obj = ViewerDetails.objects.get(cast=meeting_obj)
                    force_listen = viewer_obj.force_listen_only
                    screen_share = viewer_obj.enable_screen_sharing
                    webcam = viewer_obj.enable_webcam
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              meeting_obj.attendee_password,
                                              force_listen_only=force_listen,
                                              enable_screen_sharing=screen_share,
                                              enable_webcam=webcam
                                              )
                    meeting_obj.join_count = meeting_obj.join_count + 1
                    meeting_obj.save(update_fields=['join_count'])
                    if email != "":
                        if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                            joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                            joinee_obj.joined = True
                            joinee_obj.save()
                    return Response({'status': True,
                                     'url': result}
                                    )
                else:
                    message = "incorrect password"
                    return Response({'status': False,
                                     'message': message},
                                    status=HTTP_400_BAD_REQUEST
                                    )
            elif send_otp == True:
                try:
                    role = invitee_obj.get(email=email, verified= 'True').role
                except ObjectDoesNotExist:
                    return Response({
                        "status": False,
                        "message": "invalid user or OTP not verified"
                    }, status=HTTP_400_BAD_REQUEST)
                if role == "co-host":
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              meeting_obj.moderator_password,
                                              force_listen_only=False,
                                              enable_screen_sharing=True,
                                              enable_webcam=True
                                              )
                    meeting_obj.join_count = meeting_obj.join_count + 1
                    meeting_obj.save(update_fields=['join_count'])
                    if email != "":
                        if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                            joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                            joinee_obj.joined = True
                            joinee_obj.save()
                    return Response({'status': True,
                                     'url': result}
                                    )
                elif role == "participant":
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              meeting_obj.attendee_password,
                                              force_listen_only=False,
                                              enable_screen_sharing=True,
                                              enable_webcam=True
                                              )
                    meeting_obj.join_count = meeting_obj.join_count + 1
                    meeting_obj.save(update_fields=['join_count'])
                    if email != "":
                        if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                            joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                            joinee_obj.joined = True
                            joinee_obj.save()
                    return Response({'status': True,
                                     'url': result}
                                    )
                elif role == "viewer":
                    viewer_obj = ViewerDetails.objects.get(cast=meeting_obj)
                    force_listen = viewer_obj.force_listen_only
                    screen_share = viewer_obj.enable_screen_sharing
                    webcam = viewer_obj.enable_webcam
                    result = Meeting.join_url(private_meeting_id,
                                              name,
                                              meeting_obj.attendee_password,
                                              force_listen_only=force_listen,
                                              enable_screen_sharing=screen_share,
                                              enable_webcam=webcam
                                              )
                    meeting_obj.join_count = meeting_obj.join_count + 1
                    meeting_obj.save(update_fields=['join_count'])
                    if email != "":
                        if CastInviteeDetails.objects.filter(cast=meeting_obj, email=email).exists():
                            joinee_obj = CastInviteeDetails.objects.get(cast=meeting_obj, email=email)
                            joinee_obj.joined = True
                            joinee_obj.save()
                    return Response({'status': True,
                                     'url': result}
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


