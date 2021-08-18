from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

class event_status(APIView):
    def get(self, request):
        public_meeting_id = request.GET.get('public_meeting_id')
        try:
            private_meeting_id = Meeting.objects.get(public_meeting_id=public_meeting_id)
            result = Meeting.is_running(private_meeting_id)
            return Response({'status': True,
                             'meeting_running': result}
                            )
        except ObjectDoesNotExist:
            return Response({"status": False,
                             "message": "meeting id does not exist"},
                             status=status.HTTP_400_BAD_REQUEST
                            )