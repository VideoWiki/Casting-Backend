from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from api.global_variable import BASE_URL

class scheduled_meetings(APIView):
    def get(self, request):
        meeting = Meeting
        scheduled_meetings = meeting.objects.filter().all().order_by('-schedule_time')
        a = list(scheduled_meetings)
        l = []
        for i in a:
            name = i.event_name
            day = i.schedule_time.date()
            time = i.schedule_time.time()
            description = i.short_description
            session_key = i.public_meeting_id
            event_id = i.id
            event_creator_name = i.event_creator_name
            event_creator_id = i.user_id
            # logo = BASE_URL + "/media/" + str(i.logo)
            logo_obj = i.logo
            if logo_obj == "https://class.video.wiki/images/VideoWiki_Logo.svg":
                logo = logo_obj
            else:
                logo = BASE_URL + logo_obj.url
            if i.cover_image != "https://api.cast.video.wiki/static/alt.png":
                c_i = BASE_URL + "/media/" + str(i.cover_image)
            else:
                c_i = i.cover_image
            d = {"event_name": name, "meeting_day": day,
                 "meeting_time": time, "description": description,
                 "session_key": session_key, "event_id": event_id,
                 "creator_name": event_creator_name, "creator_id": event_creator_id,
                 "logo": str(logo),
                 "cover_image": str(c_i)}
            l.append(d)
        return Response({"status": True, "scheduled_meetings": l})