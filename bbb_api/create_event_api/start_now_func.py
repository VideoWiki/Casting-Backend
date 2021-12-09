from ..models import Meeting
from bbb_api.join_event_api.views import event_scheduler
import requests, json


def start_cast_now(public_meeting_id, name):
    meeting_obj = Meeting.objects.get(public_meeting_id=public_meeting_id)
    private_meeting_id = meeting_obj.private_meeting_id
    meeting_type = meeting_obj.meeting_type

    if meeting_type == 'public':
        print(private_meeting_id, name, meeting_obj.moderator_password)
        event_scheduler(private_meeting_id)
        result = Meeting.join_url(private_meeting_id,
                                  name,
                                  meeting_obj.moderator_password, avatar_url="")
        return result
    else:
        duration = meeting_obj.duration
        if duration == 0:
            duration = 1440
        event_scheduler(private_meeting_id)
        result = Meeting.join_url(private_meeting_id,
                                  name,
                                  meeting_obj.moderator_password,
                                  avatar_url="")
        if meeting_obj.is_streaming == True:
            if meeting_obj.bbb_stream_url_youtube != None and meeting_obj.bbb_stream_url_youtube != "":
                s_url = str(meeting_obj.bbb_stream_url_youtube)
            else:
                s_url = str(meeting_obj.bbb_stream_url_vw)
            print(s_url, type(s_url),"surl")
            if s_url == "" or "None":
                return result
            url_status = "https://api.stream.video.wiki/api/cast/live/status"
            payload = {'meeting_id': str(private_meeting_id)}
            files = []
            headers = {}
            response1 = requests.request("POST", url_status, headers=headers, data=payload, files=files)
            sp = response1.text.split(":")
            print(sp,"sp")
            sp2 = sp[1].split(",")
            if sp2[0] == 'true':
                url = "https://api.stream.video.wiki/api/cast/live/end"
                payload = {'meeting_id': '{}'.format(private_meeting_id)}
                files = []
                headers = {}
                response2 = requests.request("POST", url, headers=headers, data=payload, files=files)
            stream_dict = {
                "TZ": "Europe/Vienna",
                "BBB_RESOLUTION": str(meeting_obj.bbb_resolution),
                "BBB_START_MEETING": "false",
                "BBB_MEETING_ID": str(meeting_obj.private_meeting_id),
                "BBB_STREAM_URL": s_url,
                "BBB_SHOW_CHAT": "false",
                "BBB_USER_NAME": "Live",
                "BBB_MODERATOR_PASSWORD": str(meeting_obj.moderator_password),
                "BBB_CHAT_MESSAGE": "Welcome to the stream"
            }
            url = "https://api.stream.video.wiki/api/cast/live/start"
            headers = {
                'Content-Type': 'application/json'
            }
            r = requests.post(url, data=json.dumps(stream_dict), headers=headers)
            return result
        return result


