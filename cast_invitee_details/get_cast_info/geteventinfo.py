import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.global_variable import BASE_URL, VERIFY_API_KEY_URL
from bbb_api.models import Meeting
from cast_invitee_details.models import CastInviteeDetails


class GetOnlyEventInfo(APIView):

    def get(self, request):
        api_key = request.GET.get('apikey')
        payload = {'api_key': str(api_key)}
        files = []
        headers = {}
        response = requests.post(VERIFY_API_KEY_URL, headers=headers, data=payload, files=files)
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

            # Invitee Information
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
            if rawtime is not None:
                split_obj = rawtime.split("~")
                if len(split_obj) == 1:
                    split_obj = ["", ""]
            else:
                split_obj = ["", ""]

            data = {
                "event_name": cast_object.event_name,
                "description": cast_object.description,
                "cast_type": cast_object.meeting_type,
                "invitee_list": inv_list,
                "schedule_time": split_obj[0],
                "timezone": split_obj[1],
                "otp_private": cast_object.send_otp,
                "logo": logo,
                "cover_image": c_i,
                "back_image": cast_object.back_image,
                "primary_color": cast_object.primary_color,
                "welcome_text": cast_object.welcome,
                "banner_text": cast_object.banner_text,
                "duration": cast_object.duration,
                "logout_url": cast_object.logout_url,
                "is_streaming": cast_object.is_streaming,
                "public_stream": cast_object.public_stream,
                "bbb_stream_url": cast_object.bbb_stream_url_vw,
                "record": cast_object.record,
                "viewer_mode": cast_object.viewer_mode
            }

            return Response({"status": True, "details": data})
