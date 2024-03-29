from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from library.helper import user_info
from datetime import timedelta, datetime
from api.global_variable import BASE_URL

class get_my_events(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_id = user_info(str(token))
        user_meetings = Meeting.objects.filter(user_id=user_id).all().order_by('-schedule_time')
        my_event_list = []
        scheduled_event_list = []
        events = Meeting.objects.filter(schedule_time__gt=datetime.now() + timedelta(minutes=-30))
        for i in events:
            event = i.event_name
            scheduled_event_list.append(event)
        for i in events:
            name = i.event_name
            scheduled_event_list.append(name)
        for event in user_meetings:
            event_name = event.event_name
            event_password = event.moderator_password
            event_date = event.schedule_time.date()
            event_time = event.schedule_time.time()
            private_meeting_id = event.private_meeting_id
            event.is_running = Meeting.is_meeting_running(private_meeting_id)
            is_running = event.is_running
            public_meeting_id = event.public_meeting_id
            event_id = event.id
            short_description = event.short_description
            if event.cover_image != "https://api.cast.video.wiki/static/alt.png":
                c_i = BASE_URL + "/media/" + str(event.cover_image)
            else:
                c_i = event.cover_image
            if event.event_name in scheduled_event_list:
                event_expired = False
            else:
                event_expired = True
            result = Meeting.get_recordings(event.private_meeting_id)
            if result == None:
                recording_available = False
            else:
                recording_available = True
            my_event_list.append({"event_name": event_name,
                                  "moderator_password": event_password,
                                  "event_date": event_date,
                                  "event_time": event_time,
                                  "is_running": is_running,
                                  "event_expired": event_expired,
                                  "public_meeting_id": public_meeting_id,
                                  "event_id": event_id,
                                  "short_description": short_description,
                                  "cover_image": str(c_i),
                                  "recording_available": recording_available
                         })
        return Response({"status": True,
                         "my_events": my_event_list
                         })