from bbb_api.models import Meeting
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
import datetime
from bbb_api.create_event_email_sender import tc
import pytz, ast
from api.global_variable import VW_RTMP_URL
from bbb_api.models import ViewerDetails
from library.helper import user_info

class update_cast(APIView):
    def patch(self, request):
        cast_id = request.data["cast_id"]
        cast_object = Meeting.objects.get(public_meeting_id=cast_id)
        cast_name = request.data["cast_name"]
        description = request.data["description"]
        cast_type = request.data["cast_type"]
        collect_attendee_email = request.data["collect_attendee_email"]
        private_otp = request.data["private_otp"]
        schedule_time = request.data["schedule_time"]
        timezone = request.data["timezone"]

        logo = request.data["logo"]
        if logo == "":
            logo = "https://class.video.wiki/images/VideoWiki_Logo.svg"
        else:
            logo = logo
        cover_image = request.data["cover_image"]
        if cover_image != "":
            cover_image = cover_image
        else:
            cover_image = "https://api.cast.video.wiki/static/alt.png"
        primary_color = request.data["primary_color"]
        welcome_text = request.data["welcome_text"]
        banner_text = request.data["banner_text"]
        guest_policy = request.data["guest_policy"]
        moderator_only_text = request.data["moderator_only_text"]
        duration = request.data["duration"]
        logout_url = request.data["logout_url"]

        is_streaming = request.data["is_streaming"]
        public_stream = request.data["public_stream"]
        bbb_stream_url = request.data["bbb_stream_url"]

        record = request.data["record"]
        password_auth = request.data["password_auth"]
        end_when_no_moderator = request.data["end_when_no_moderator"]
        allow_moderator_to_unmute_user = request.data["allow_moderator_to_unmute_user"]
        auto_start_recording = request.data["auto_start_recording"]
        mute_on_start = request.data["mute_on_start"]
        webcam_only_for_moderator = request.data["webcam_only_for_moderator"]
        disable_cam = request.data["disable_cam"]
        disable_mic = request.data["disable_mic"]
        lock_layout = request.data["lock_layout"]
        viewer_mode = request.data["viewer_mode"]
        user_id = cast_object.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass
        if curr_user_id == user_id:

            cast_object.event_name = cast_name
            cast_object.description = description
            cast_object.meeting_type = cast_type
            cast_object.public_otp = collect_attendee_email
            cast_object.send_otp = private_otp
            cast_object.raw_time = schedule_time + "~" + timezone
            ct = tc(schedule_time, timezone)
            time_now = datetime.datetime.now().astimezone(pytz.utc)
            if time_now > ct:
                return Response({
                    "status": False,
                    "message": "invalid schedule time"}, status=status.HTTP_400_BAD_REQUEST)
            cast_object.schedule_time = ct

            if is_streaming == 'True':
                bool_is_streaming = True
            else:
                bool_is_streaming = False
            cast_object.is_streaming = bool_is_streaming
            stream_urls_list = []
            if bool_is_streaming == True:
                bbb_resolution = "1280x720"
                cast_object.bbb_resolution = bbb_resolution
                stream_urls = bbb_stream_url
                converted_stream_urls = ast.literal_eval(stream_urls)
                if converted_stream_urls[0]["vw_stream"] == 'True':
                    url = "{}{}".format(VW_RTMP_URL, cast_object.public_meeting_id)
                    stream_urls_list.append(url)
                if len(converted_stream_urls[1]["urls"]) > 0:
                    for i in converted_stream_urls[1]["urls"]:
                        stream_urls_list.append(i)
                cast_object.bbb_stream_url_vw = stream_urls_list
                cast_object.public_stream = public_stream


            cast_object.logo = logo
            cast_object.cover_image = cover_image
            cast_object.primary_color = primary_color
            cast_object.welcome = welcome_text
            cast_object.banner_text = banner_text
            cast_object.guest_policy = guest_policy
            cast_object.moderator_only_text = moderator_only_text
            cast_object.duration = duration
            cast_object.logout_url = logout_url

            cast_object.record = record
            cast_object.password_auth = password_auth
            cast_object.end_when_no_moderator = end_when_no_moderator
            cast_object.allow_moderator_to_unmute_user = allow_moderator_to_unmute_user
            cast_object.auto_start_recording = auto_start_recording
            cast_object.mute_on_start = mute_on_start
            cast_object.webcam_only_for_moderator = webcam_only_for_moderator
            cast_object.disable_cam = disable_cam
            cast_object.disable_mic = disable_mic
            cast_object.lock_layout = lock_layout
            cast_object.viewer_mode = viewer_mode
            if viewer_mode == 'True':
                force_listen_only = True
                enable_webcam = False
                enable_screen_sharing = False
                try:
                    viewer_obj = ViewerDetails.objects.get(cast=cast_object)
                    viewer_obj.force_listen_only = force_listen_only
                    viewer_obj.enable_webcam = enable_webcam
                    viewer_obj.enable_screen_sharing = enable_screen_sharing
                    viewer_obj.save()
                except ObjectDoesNotExist:
                    ViewerDetails.objects.create(cast=cast_object,
                                                 force_listen_only=force_listen_only,
                                                 enable_webcam=enable_webcam,
                                                 enable_screen_sharing=enable_screen_sharing)
            if viewer_mode == 'False':
                try:
                    viewer_obj = ViewerDetails.objects.get(cast=cast_object)
                    viewer_obj.delete()
                except ObjectDoesNotExist:
                    pass



            cast_object.save()
            return Response({'status': True, 'message': 'cast updated successfully'})
        else:
            return Response({'status': False, 'message': 'Unable to update cast'},
                            status=status.HTTP_400_BAD_REQUEST)