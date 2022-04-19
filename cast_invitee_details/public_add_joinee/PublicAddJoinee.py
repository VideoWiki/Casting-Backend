from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist


class PublicAddJoinee(APIView):
    def post(self, request):
        cast_id = request.data["session_id"]
        name = request.data["user_name"]
        email = request.data["user_email"]
        email = email.lower()
        if cast_id == "":
            return Response({
                "status": False,
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid session_id"
            }, status=status.HTTP_400_BAD_REQUEST)
        mode_viewer = cast_obj.viewer_mode
        if mode_viewer == True:
            role = "viewer"
        elif mode_viewer == False:
            role = "participant"
        if email !="":
            print("1")
            if not CastInviteeDetails.objects.filter(cast=cast_obj, email=email).exists():
                CastInviteeDetails.objects.create(cast=cast_obj,
                                                  name= name,
                                                  email= email,
                                                  invited= False,
                                                  role= role,
                                                  mint='not started')
        else:
            CastInviteeDetails.objects.create(cast=cast_obj, name=name, invited=False, role= role, mint='not started')

        return Response({
            "status": True,
            "message": "successful"
        })