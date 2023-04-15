from bbb_api.models import Meeting
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from api.global_variable import BASE_URL
from library.helper import user_info

class get_details(APIView):
    def get(self, request):
        cast_id = request.GET.get("cast_id")
        try:
            cast_object = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "cast not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        user_id = cast_object.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass

        if curr_user_id == user_id:
            logo_obj = cast_object.logo
            if logo_obj == "https://class.video.wiki/images/VideoWiki_Logo.svg":
                logo = str(logo_obj)
            elif logo_obj == "":
                logo = None
            elif str(logo_obj).startswith(BASE_URL):
                # logo = str(logo_obj)
                logo = str(cast_object.logo)
            else:
                # logo = BASE_URL + logo_obj.url
                logo = str(cast_object.logo)

            if cast_object.cover_image == "https://api.cast.video.wiki/static/alt.png":
                c_i = BASE_URL + "/media/" + str(cast_object.cover_image)
            elif str(cast_object.cover_image).startswith(BASE_URL):
                c_i = str(cast_object.cover_image)
            else:
                c_i = str(cast_object.cover_image)
            rawtime = cast_object.raw_time
            if rawtime != None:
                split_obj = rawtime.split("~")
                if len(split_obj) == 1:
                    split_obj = ["", ""]
            else:
                split_obj = ["", ""]
            data = {
                "event_name": cast_object.event_name,
                "description": cast_object.description,
                "cast_type": cast_object.meeting_type,
                "collect_attendee_email": cast_object.public_otp,
                "schedule_time": split_obj[0],
                "timezone": split_obj[1],
                "otp_private": cast_object.send_otp,

                "logo": logo,
                "cover_image": c_i,
                "primary_color": cast_object.primary_color,
                "welcome_text": cast_object.welcome,
                "banner_text": cast_object.banner_text,
                "guest_policy": cast_object.guest_policy,
                "moderator_only_text": cast_object.moderator_only_text,
                "duration": cast_object.duration,
                "logout_url": cast_object.logout_url,

                "is_streaming": cast_object.is_streaming,
                "public_stream": cast_object.public_stream,
                "bbb_stream_url": cast_object.bbb_stream_url_vw,

                "record": cast_object.record,
                "password_auth": cast_object.password_auth,
                "end_when_no_moderator": cast_object.end_when_no_moderator,
                "allow_moderator_to_unmute_user": cast_object.allow_moderator_to_unmute_user,
                "auto_start_recording": cast_object.auto_start_recording,
                "mute_on_start": cast_object.mute_on_start,
                "webcam_only_for_moderator": cast_object.webcam_only_for_moderator,
                "disable_cam": cast_object.disable_cam,
                "disable_mic": cast_object.disable_mic,
                "lock_layout": cast_object.lock_layout,
                "viewer_mode": cast_object.viewer_mode,
                "back_image": cast_object.back_image
            }

            return Response({"status": True, "details": data})
        else:
            return Response({"status": False,
                             "message": "user validation error"}, status=status.HTTP_400_BAD_REQUEST)