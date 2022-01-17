from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

class CastRecording(APIView):
    def get(self, request):
        cast_id = request.GET.get("cast_id")
        try:
            cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid cast id"
            }, status=status.HTTP_400_BAD_REQUEST)
        result = Meeting.get_recordings(cast_obj.private_meeting_id)
        if result != None:
            vid_url = result
            status_code = status.HTTP_200_OK
            message = True
        else:
            vid_url = None
            status_code = status.HTTP_400_BAD_REQUEST
            message = False
        return Response({
            "status": message,
            "recording_url": vid_url
        }, status=status_code)