from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

class meeting_type_checker(APIView):
    def get(self, request):
        session_key = request.GET.get('session_key')
        try:
            get_model = Meeting.objects.get(public_meeting_id=session_key)
            type = get_model.meeting_type
        except ObjectDoesNotExist:
            return Response({"status": False,
                             "message": "incorrect session key"},
                              status=status.HTTP_400_BAD_REQUEST)

        if type == "public":
            return Response({"status": True,
                             "event_type": type})
        else:
            return Response({"status": True,
                             "event_type": type})