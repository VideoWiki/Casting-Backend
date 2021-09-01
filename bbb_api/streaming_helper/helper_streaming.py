import django.utils.timezone
from bbb_api.models import Meeting
import requests


def stream_status():
    meetings = Meeting.objects.all().order_by('-schedule_time')
    current_date = django.utils.timezone.now().date()
    my_event_list = []
    scheduled_event_list = []
    events = Meeting.objects.filter(schedule_time__gt=django.utils.timezone.now()).all()
    print(events,"pp")
    for i in events:
        event = i.private_meeting_id
        scheduled_event_list.append(event)
    for i in events:
        private_meeting_id = i.private_meeting_id
        name = i.event_name
        event = Meeting.is_meeting_running(private_meeting_id=private_meeting_id)
        print(event, "rnrnrn")
        scheduled_event_list.append(name)
    print(scheduled_event_list, "11")
    expired_list = []
    for event in meetings:
        if event.event_name in scheduled_event_list:
            event_expired = False
        else:
            event_expired = True
            event_running = Meeting.is_meeting_running(private_meeting_id=event.private_meeting_id)
            print(event_running, event.private_meeting_id)
            if event_running == "false":
                today = event.schedule_time.date()
                if current_date == today:
                    expired_list.append(event.private_meeting_id)

    end_list = []
    print(expired_list)
    for i in expired_list:
        obj = Meeting.objects.get(private_meeting_id=i).is_streaming
        if obj == True:
            end_list.append(i)
    for i in expired_list:
        print(i)
        url = "https://api.stream.video.wiki/api/cast/live/status"

        payload = {'meeting_id': str(i)}
        files = []
        headers = {}

        response1 = requests.request("POST", url, headers=headers, data=payload, files=files)
        print(response1.text)
        sp = response1.text.split(":")
        sp2 = sp[1].split(",")
        if sp2[0] == 'true':
            url = "https://api.stream.video.wiki/api/cast/live/end"
            payload = {'meeting_id': '{}'.format(i)}
            files = []
            headers = {}
            response2 = requests.request("POST", url, headers=headers, data=payload, files=files)
            print(response2.text)

    return "True"
