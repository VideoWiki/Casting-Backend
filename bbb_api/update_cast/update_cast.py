from bbb_api.models import Meeting
from rest_framework.views import APIView
from rest_framework.response import Response
from library.helper import user_info
from rest_framework import status
import datetime
from bbb_api.create_event_email_sender import time_convertor
from cast_invitee_details.models import CastInviteeDetails
import json
import ast

class update_cast(APIView):
    def post(self, request):
        cast_id = request.data["cast_id"]
        cast_object = Meeting.objects.get(public_meeting_id=cast_id)
        cast_name = request.data["cast_name"]
        welcome_text = request.data["welcome_text"]
        description = request.data["description"]
        short_description = request.data["short_description"]
        max_participant = request.data["max_participant"]
        record = request.data["record"]
        duration = request.data["duration"]
        mute_on_start = request.data["mute_on_start"]
        attendee_password = request.data["attendee_password"]
        moderator_password = request.data["moderator_password"]
        banner_text = request.data["banner_text"]
        logo = request.data["logo"]
        guest_policy = request.data["guest_policy"]
        end_when_no_moderator = request.data["end_when_no_moderator"]
        allow_moderator_to_unmute_user = request.data["allow_moderator_to_unmute_user"]
        webcam_only_for_moderator = request.data["webcam_only_for_moderator"]
        auto_start_recording = request.data["auto_start_recording"]
        allow_start_stop_recording = request.data["allow_start_stop_recording"]
        disable_cam = request.data["disable_cam"]
        disable_mic = request.data["disable_mic"]
        logout_url = request.data["logout_url"]
        lock_layout = request.data["lock_layout"]
        lock_on_join = request.data["lock_on_join"]
        hide_users = request.data["hide_users"]
        primary_color = request.data["primary_color"]
        secondary_color = request.data["secondary_color"]
        back_image = request.data["back_image"]
        event_tag = request.data["event_tag"]
        cover_image = request.data["cover_image"]
        is_streaming = request.data["is_streaming"]
        vw_stream_url = request.data["vw_stream_url"]
        bbb_stream_url_youtube = request.data["bbb_stream_url_youtube"]
        schedule_time = request.data["schedule_time"]
        invitee_details = request.data["invitee_details"]
        user_id = cast_object.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass
        if curr_user_id == user_id:

            cast_object.event_name = cast_name
            cast_object.welcome = welcome_text
            cast_object.description = description
            cast_object.short_description = short_description
            cast_object.max_participant = max_participant
            cast_object.record = record
            cast_object.duration = duration
            cast_object.mute_on_start = mute_on_start
            cast_object.attendee_password = attendee_password
            cast_object.moderator_password = moderator_password
            cast_object.banner_text = banner_text
            cast_object.logo = logo
            cast_object.guest_policy = guest_policy
            cast_object.end_when_no_moderator = end_when_no_moderator
            cast_object.allow_moderator_to_unmute_user = allow_moderator_to_unmute_user
            cast_object.webcam_only_for_moderator = webcam_only_for_moderator
            cast_object.auto_start_recording = auto_start_recording
            cast_object.allow_start_stop_recording = allow_start_stop_recording
            cast_object.disable_cam = disable_cam
            cast_object.disable_mic = disable_mic
            cast_object.logout_url = logout_url
            cast_object.lock_layout = lock_layout
            cast_object.lock_on_join = lock_on_join
            cast_object.hide_users = hide_users
            cast_object.primary_color = primary_color
            cast_object.secondary_color = secondary_color
            cast_object.back_image = back_image
            cast_object.event_tag = event_tag
            cast_object.cover_image = cover_image
            cast_object.is_streaming = is_streaming
            if vw_stream_url == 'True':
                url = "rtmp://play.stream.video.wiki/stream/{}".format(cast_object.public_meeting_id)
                cast_object.bbb_stream_url_vw = url
            else:
                cast_object.bbb_stream_url_vw = None
            cast_object.bbb_stream_url_youtube = bbb_stream_url_youtube
            cast_object.raw_time = schedule_time
            converted_time = time_convertor(schedule_time)
            time_now = datetime.datetime.now()
            if time_now > converted_time:
                return Response({
                    "status": False,
                    "message": "invalid schedule time"}, status=status.HTTP_400_BAD_REQUEST)
            cast_object.schedule_time = converted_time

            cast_inv_obj = CastInviteeDetails.objects.filter(cast=cast_object)
            if cast_inv_obj != None:
                for i in cast_inv_obj:
                    i.delete()
            m_list = ast.literal_eval(invitee_details)
            for i in m_list:
                CastInviteeDetails.objects.create(cast=cast_object, name=i["name"], email=i["email"], role=i["type"])
            cast_object.save()
            return Response({'status': True, 'message': 'cast updated successfully'})
        else:
            return Response({'status': False, 'message': 'Unable to update cast'},
                            status=status.HTTP_400_BAD_REQUEST)