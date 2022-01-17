from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist

class CheckEmail(APIView):
    def get(self, request):
        email = request.GET.get("email")
        public_meeting_id = request.GET.get("cast_id")

        if public_meeting_id == "" or email=="":
            return Response({
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            cast_obj = Meeting.objects.get(public_meeting_id=public_meeting_id)
        except ObjectDoesNotExist:
            return Response({
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)

        email_obj = CastInviteeDetails.objects.filter(cast=cast_obj)
        list_email = []

        for i in email_obj:
            list_email.append(i.email)

        if email in list_email:
            status_bool = False
            duplicate_email = True
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            status_bool = True
            duplicate_email = False
            status_code = status.HTTP_200_OK

        return Response({
            "status": status_bool,
            "duplicate_email": duplicate_email
        }, status=status_code)