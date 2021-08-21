from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from library.helper import user_info


class event_recording(APIView):
    def get(self, request):
        meeting_id = request.GET.get("meeting_id")
        pvt_meet_id = Meeting.objects.get(public_meeting_id=meeting_id).private_meeting_id
        result = Meeting.get_recordings(private_meeting_id=pvt_meet_id)
        print(result)
        if result != None:
            return Response({"status": True, "url": result})
        return Response({"status": False, "url": None})
