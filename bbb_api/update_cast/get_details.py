from bbb_api.models import Meeting
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from library.helper import user_info
from django.core.exceptions import ObjectDoesNotExist
from api.global_variable import BASE_URL
from cast_invitee_details.models import CastInviteeDetails

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
                logo = logo_obj
            elif logo_obj == "":
                logo = None
            else:
                logo = BASE_URL + logo_obj.url

            if cast_object.cover_image != "https://api.cast.video.wiki/static/alt.png":
                c_i = BASE_URL + "/media/" + str(cast_object.cover_image)
            else:
                c_i = str(cast_object.cover_image)
            inv_list = []
            cast_invite_object = CastInviteeDetails.objects.filter(cast=cast_object)
            if cast_invite_object.count() != 0:
                for i in cast_invite_object:
                    name = i.name
                    role = i.role
                    email = i.email
                    d = {
                        "name": name,
                        "role": role,
                        "email": email
                    }
                    inv_list.append(d)
            data = {
                "event_name": cast_object.event_name,
                "welcome_text": cast_object.welcome,
                "description": cast_object.description,
                "short_description": cast_object.short_description,
                "max_participant": cast_object.max_participant,
                "record": cast_object.record,
                "duration": cast_object.duration,
                "mute_on_start": cast_object.mute_on_start,
                "attendee_password": cast_object.attendee_password,
                "moderator_password": cast_object.moderator_password,
                "banner_text": cast_object.banner_text,
                "logo": logo,
                "guest_policy": cast_object.guest_policy,
                "end_when_no_moderator": cast_object.end_when_no_moderator,
                "allow_moderator_to_unmute_user": cast_object.allow_moderator_to_unmute_user,
                "webcam_only_for_moderator": cast_object.webcam_only_for_moderator,
                "auto_start_recording": cast_object.auto_start_recording,
                "allow_start_stop_recording": cast_object.allow_start_stop_recording,
                "disable_cam": cast_object.disable_cam,
                "disable_mic": cast_object.disable_mic,
                "logout_url": cast_object.logout_url,
                "lock_layout": cast_object.lock_layout,
                "lock_on_join": cast_object.lock_on_join,
                "hide_users": cast_object.hide_users,
                "primary_color": cast_object.primary_color,
                "secondary_color": cast_object.secondary_color,
                "back_image": cast_object.back_image,
                "event_tag": cast_object.event_tag,
                "cover_image": c_i,
                "is_streaming": cast_object.is_streaming,
                "bbb_stream_url_youtube": cast_object.bbb_stream_url_youtube,
                "schedule_time": cast_object.raw_time,
                "invitee_details": inv_list
            }

            return Response({"status": True, "details": data})
        else:
            return Response({"status": False,
                             "message": "user validation error"}, status=status.HTTP_400_BAD_REQUEST)