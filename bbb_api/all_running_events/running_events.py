from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from ..models import Meeting
import time

class meetings(APIView):
    def get(self, request):
        print("here")
        meetings = Meeting.get_meetings()
        if len(meetings) == 0:
            return Response({'status': False, 'meetings': None, 'message': 'no meeting is running currently'})
        l = []
        for i in meetings:
            name = i['name']
            print(name)
            running = i['running']
            participant_count = i['info']['participant_count']
            start_time = i['info']['start_time']
            sec_time = int(start_time) / 1000
            date = time.strftime("%Y-%m-%d", time.gmtime(sec_time))
            time_hms = time.strftime("%H:%M:%S", time.gmtime(sec_time))
            max_users = i['info']['max_users']
            meet_obj = Meeting.objects.get(event_name=name)
            short_description = meet_obj.short_description
            event_creator_name = meet_obj.event_creator_name
            event_tag = meet_obj.event_tag
            pub_meet_id = meet_obj.public_meeting_id
            dict = {"event_name": name,
                    "running": running,
                    "participant_count": participant_count,
                    "date": date,
                    "time": time_hms,
                    "max_users": max_users,
                    "short_description": short_description,
                    "event_creator_name": event_creator_name,
                    "event_tag": event_tag,
                    "public_meeting_id": pub_meet_id,
                    "event_duration": meet_obj.duration
                    }
            l.append(dict)
        return Response({'status': True, 'meetings': l})