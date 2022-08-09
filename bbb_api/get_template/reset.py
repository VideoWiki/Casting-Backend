import json
from rest_framework.views import APIView
from ..models import Meeting, MailTemplateDetails
from rest_framework.response import Response
from library.helper import user_info
from rest_framework.status import HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta
import requests
from cast_invitee_details.models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist
from api.global_variable import CLIENT_DOMAIN_URL, VW_RTMP_URL
import ast


class ResetTemplate(APIView):
    def patch(self, request):
        cast_id = request.data['cast_id']
        role = request.data['role']
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
        name = cast_obj.event_name
        schedule_time = cast_obj.schedule_time
        if role == "co-host":
            body = f'''You have been invited to join a cast {name} for {schedule_time} 
                        url for Co-host: {CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_obj.public_meeting_id, cast_obj.hashed_moderator_password)} 
                        url for Participant: {CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_obj.public_meeting_id, cast_obj.hashed_attendee_password)}'''
            if cast_obj.viewer_mode == True:
                body_view = f'url for Viewer: {CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_obj.public_meeting_id, cast_obj.hashed_viewer_password)}'
                body = body + body_view
            if cast_obj.is_streaming == True:
                body_spec = f'url for Spectator: {VW_RTMP_URL + "live/{}".format(cast_obj.public_meeting_id)}'
                body = body + body_spec
            template_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
            template_obj.subject = cast_obj.event_name
            template_obj.body = body
            template_obj.save()

        elif role == "participant":
            body = f'''You have been invited to join a cast {name}, as a Participant. The cast will begin at {schedule_time}
                        url for cast: {CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_obj.public_meeting_id, cast_obj.hashed_attendee_password)}'''
            template_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
            template_obj.subject = cast_obj.event_name
            template_obj.body = body
            template_obj.save()

        if role == "viewer":
            if viewer_mode == True:
                body = f'''You have been invited to join a cast {name}, as a Viewer. The cast will begin at {schedule_time}
                            url for cast: {CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_obj.public_meeting_id, cast_obj.hashed_viewer_password)}'''
                template_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
                template_obj.subject = cast_obj.event_name
                template_obj.body = body
                template_obj.save()

        if role == "spectator":
            if cast_obj.is_streaming == True:
                body = f'''You have been invited to join a cast {name}, as a Spectator. The cast will begin at {schedule_time}
                            url for cast: {VW_RTMP_URL + "live/{}".format(cast_obj.public_meeting_id)}'''
                template_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
                template_obj.subject = cast_obj.event_name
                template_obj.body = body
                template_obj.save()

        return Response({
            "status": True,
            "message": "updated"
        })