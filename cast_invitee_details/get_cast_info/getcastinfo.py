import requests
from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST
from ..models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist
from api.global_variable import BASE_URL, CLIENT_DOMAIN_URL, VERIFY_API_KEY_URL


class GetCastInformation(APIView):

    def get(self, request):
        api_key = request.data.get('apikey')
        print(api_key, "apikey")
        payload = {'api_key': str(api_key)}
        files = []
        headers = {}
        response = requests.post(VERIFY_API_KEY_URL, headers=headers, data=payload, files=files)
        print(response.text, response.status_code, "lll")
        if response.status_code != requests.codes.ok:
            return Response({
                "message": "Invalid Api Key",
                "status": False
            }, status=HTTP_400_BAD_REQUEST)
        else:
            cast_id = request.GET.get("cast_id")
            try:
                cast_object = Meeting.objects.get(public_meeting_id=cast_id)
            except ObjectDoesNotExist:
                return Response({
                    "status": False,
                    "message": "cast not found"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Invitees information
            cast_invite_object = CastInviteeDetails.objects.filter(cast=cast_object)
            inv_list = []
            if cast_invite_object.count() != 0:
                for i in cast_invite_object:
                    id = i.id
                    role = i.role
                    email = i.email
                    otp_verified = i.verified,
                    joined = i.joined
                    d = {
                        "id": id,
                        "role": role,
                        "email": email,
                        "otp_verified": otp_verified,
                        "joined": joined
                    }
                    inv_list.append(d)
            else:
                inv_list = None

            # Join URLs
            join_urls = []
            if cast_object.meeting_type == 'public':
                join_data = {
                    "event_name": cast_object.event_name,
                    "event_creator_name": cast_object.event_name,
                    "public_meeting_id": cast_object.public_meeting_id,
                    "date": cast_object.schedule_time.date(),
                    "creator_url": {
                        CLIENT_DOMAIN_URL + "/e/creator/join/{}/?pass={}".format(cast_object.public_meeting_id,
                                                                                 cast_object.hashed_moderator_password)},
                    "participant_url": {
                        CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_object.public_meeting_id,
                                                                    cast_object.hashed_attendee_password)},
                    "co-host_url": {
                        CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_object.public_meeting_id,
                                                                    cast_object.hashed_moderator_password)},
                    "viewer_url": {
                        CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_object.public_meeting_id,
                                                                    cast_object.hashed_viewer_password)},
                    "spectator_url": {
                        CLIENT_DOMAIN_URL + "/live/{}".format(cast_object.public_meeting_id)}
                }
                join_urls.append(join_data)
            else:
                for i in cast_invite_object:
                    join_data = {
                        "event_name": cast_object.event_name,
                        "event_creator_name": cast_object.event_name,
                        "public_meeting_id": cast_object.public_meeting_id,
                        "date": cast_object.schedule_time.date(),
                    }
                    if i.role == 'co-host':
                        join_data["co-host_url"] = CLIENT_DOMAIN_URL + "/e/?email={}".format(i.email)
                    elif i.role == 'participant':
                        join_data["participant_url"] = CLIENT_DOMAIN_URL + "/e/?email={}".format(i.email)
                    elif i.role == 'viewer':
                        join_data["viewer_url"] = CLIENT_DOMAIN_URL + "/e/?email={}".format(i.email)
                    else:
                        join_data["spectator_url"] = CLIENT_DOMAIN_URL + "/live/{}".format(cast_object.public_meeting_id)
                    join_urls.append(join_data)

            logo_obj = cast_object.logo
            if logo_obj == "https://class.video.wiki/images/VideoWiki_Logo.svg":
                logo = str(logo_obj)
            elif logo_obj == "":
                logo = None
            elif str(logo_obj).startswith(BASE_URL):
                logo = str(cast_object.logo)
            else:
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
                "invitee_list": inv_list,
                "join urls": join_urls,
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
