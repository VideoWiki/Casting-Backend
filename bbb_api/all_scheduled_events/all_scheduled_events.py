from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response


class scheduled_meetings(APIView):
    def get(self, request):
        meeting = Meeting
        scheduled_meetings = meeting.objects.filter().all().order_by('-schedule_time')
        a = list(scheduled_meetings)
        l = []
        for i in a:
            name = i.name
            day = i.schedule_time.date()
            time = i.schedule_time.time()
            description = i.welcome
            session_key = i.public_meeting_id
            event_id = i.id
            d = {"meeting_name": name, "meeting_day": day,
                 "meeting_time": time, "description": description,
                 "session_key": session_key, "event_id": event_id}
            l.append(d)
        return Response({"status": True, "scheduled_meetings": l})