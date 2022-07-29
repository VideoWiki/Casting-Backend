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


class MagicUrl(APIView):
    def post(self, request):
        cast_id = request.data['id']
        cast_key = request.data['pass']
        name = request.data['name']
        if cast_id == "":
            return Response({
                "message": "invalid cast id",
                "status": False
            }, status=HTTP_400_BAD_REQUEST)
        try:
            cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "message": "invalid cast id",
                "status": False
            },status=HTTP_400_BAD_REQUEST)
        hashed_pub_key = cast_obj.hashed_attendee_password
        hashed_mod_key = cast_obj.hashed_moderator_password
        viewer_mode = cast_obj.viewer_mode
        cast_type = cast_obj.meeting_type
        if cast_type == 'public':
            pass
        else:
            return Response({
                "message": "invalid cast id",
                "status": False
            }, status=HTTP_400_BAD_REQUEST)
        if viewer_mode == True:
            hashed_view_key = cast_obj.hashed_viewer_password
            if cast_key == hashed_view_key:
                viewer_obj = ViewerDetails.objects.get(cast=cast_obj)
                force_listen = viewer_obj.force_listen_only
                screen_share = viewer_obj.enable_screen_sharing
                webcam = viewer_obj.enable_webcam
                result = Meeting.join_url(cast_obj.private_meeting_id,
                                          name,
                                          cast_obj.attendee_password,
                                          force_listen_only=force_listen,
                                          enable_screen_sharing=screen_share,
                                          enable_webcam=webcam
                                          )
                cast_obj.join_count = cast_obj.join_count + 1
                cast_obj.save(update_fields=['join_count'])
                return Response({'status': True,
                                 'url': result}
                                )
        print(hashed_pub_key, hashed_mod_key, viewer_mode)
        status = Meeting.is_meeting_running(cast_obj.private_meeting_id)
        if status == "false":
            message = "the cast you are trying to join has either ended or yet to begin"
            return Response({'status': False,
                             'message': message},
                            status=HTTP_400_BAD_REQUEST
                            )
        else:
            pass
        if cast_key == hashed_pub_key:
            result = Meeting.join_url(cast_obj.private_meeting_id,
                                      name,
                                      cast_obj.attendee_password,
                                      force_listen_only=False,
                                      enable_screen_sharing=True,
                                      enable_webcam=True
                                      )
            cast_obj.join_count = cast_obj.join_count + 1
            cast_obj.save(update_fields=['join_count'])
            return Response({'status': True,
                             'url': result}
                            )
        elif cast_key == hashed_mod_key:
            result = Meeting.join_url(cast_obj.private_meeting_id,
                                      name,
                                      cast_obj.moderator_password,
                                      force_listen_only=False,
                                      enable_screen_sharing=True,
                                      enable_webcam=True
                                      )
            cast_obj.join_count = cast_obj.join_count + 1
            cast_obj.save(update_fields=['join_count'])
            return Response({'status': True,
                             'url': result}
                            )


        return Response({
            "status": True
        })

