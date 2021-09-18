from .models import CastInviteeDetails
from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
# Create your views here.

class add_invitees(APIView):
    def post(self, request):
        cast_id = request.data["cast_id"]
        obj = Meeting.objects.get(public_meeting_id=cast_id)
        if id != None:
            CastInviteeDetails.cast_id = cast_id
            invitee_list = request.data['invitee_list']
            for i in invitee_list:
                CastInviteeDetails.objects.create(cast=obj, name=i["name"], email=i["email"], role=i["type"])
            return Response({"status": True})
        return Response({"status": False})







