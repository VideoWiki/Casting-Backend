import json
from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from library.helper import user_info
from rest_framework.status import HTTP_400_BAD_REQUEST
import requests
from django.core.exceptions import ObjectDoesNotExist
import ast


class start_stream(APIView):
    def get(self, request):
        public_meeting_id = request.GET.get('cast_id')

        try:
            meet_obj = Meeting.objects.get(public_meeting_id=public_meeting_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid cast id"
            }, status= HTTP_400_BAD_REQUEST)

        creator_id = meet_obj.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass
        if curr_user_id == creator_id:
            if meet_obj.is_streaming == True:
                stream_urls_list = ast.literal_eval(meet_obj.bbb_stream_url_vw)
                stream_str = ","
                new_stream_str = stream_str.join(stream_urls_list)
                url_status = "https://api.stream.video.wiki/api/cast/live/status"
                payload = {'meeting_id': str(meet_obj.private_meeting_id)}
                files = []
                headers = {}
                response1 = requests.request("POST", url_status, headers=headers, data=payload, files=files)
                sp = response1.text.split(":")
                sp2 = sp[1].split(",")
                if sp2[0] == 'true':
                    url = "https://api.stream.video.wiki/api/cast/live/end"
                    payload = {'meeting_id': '{}'.format(meet_obj.private_meeting_id)}
                    files = []
                    headers = {}
                    response2 = requests.request("POST", url, headers=headers, data=payload, files=files)
                stream_dict = {
                    "TZ": "Europe/Vienna",
                    "BBB_RESOLUTION": str(meet_obj.bbb_resolution),
                    "BBB_START_MEETING": "false",
                    "BBB_MEETING_ID": str(meet_obj.private_meeting_id),
                    "BBB_STREAM_URL": new_stream_str,
                    "BBB_SHOW_CHAT": "false",
                    "BBB_USER_NAME": "Live",
                    "BBB_MODERATOR_PASSWORD": str(meet_obj.moderator_password),
                    "BBB_CHAT_MESSAGE": "Welcome to the stream"
                }
                url = "https://api.stream.video.wiki/api/cast/live/start"
                headers = {
                    'Content-Type': 'application/json'
                }
                r = requests.post(url, data=json.dumps(stream_dict), headers=headers)
                bin = r.content
                res = bin.decode(('utf-8'))
                return Response({'status': True,
                                 'response': res}
                                )
            else:
                return Response({'status': False,
                                 'response': "stream not activated"}
                                )
        else:
            return Response({
                'status': False,
                'message': 'invalid user'
            }, status= HTTP_400_BAD_REQUEST)


