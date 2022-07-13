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
from api.global_variable import CLIENT_DOMAIN_URL
import ast


class UpdateTemplate(APIView):
    def patch(self, request):
        cast_id = request.data['cast_id']
        subject = request.data['subject']
        role = request.data['role']
        body = request.data['body']
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
        template_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
        template_obj.subject = subject
        template_obj.body = body
        template_obj.save()
        return Response({
            "status": True,
            "message": "updated"
        })