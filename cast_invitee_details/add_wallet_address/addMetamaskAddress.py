from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails



class AddUser(APIView):
    def post(self, request):
        public_address = request.data["public_address"]
        public_cast_id = request.data["cast_id"]
        email = request.data["email"]

        if public_address == "" or public_cast_id == "" or email=="":
            return Response({
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)
        cast_obj = Meeting.objects.get(public_meeting_id=public_cast_id)
        obj = CastInviteeDetails.objects.filter(cast= cast_obj).all()
        email_obj = obj.get(email__exact=email)
        email_obj.metamask_address = public_address
        email_obj.save()


        return Response({
            "status": True,
        })