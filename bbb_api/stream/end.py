from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from library.helper import user_info
from rest_framework.status import HTTP_400_BAD_REQUEST
import requests
from django.core.exceptions import ObjectDoesNotExist

class end_stream(APIView):
    def get(self, request):
        public_meeting_id = request.GET.get('cast_id')

        try:
            meet_obj = Meeting.objects.get(public_meeting_id=public_meeting_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid cast id"
            }, status=HTTP_400_BAD_REQUEST)

        creator_id = meet_obj.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass
        if curr_user_id == creator_id:
            if meet_obj.is_streaming == True:
                url_status = "https://api.stream.video.wiki/api/cast/live/status"
                payload = {'meeting_id': str(meet_obj.private_meeting_id)}
                files = []
                headers = {}
                response1 = requests.request("POST", url_status, headers=headers, data=payload, files=files)
                sp = response1.text.split(":")
                sp2 = sp[1].split(",")
                res = "livestream already ended"
                if sp2[0] == 'true':
                    url = "https://api.stream.video.wiki/api/cast/live/end"
                    payload = {'meeting_id': '{}'.format(meet_obj.private_meeting_id)}
                    files = []
                    headers = {}
                    r = requests.request("POST", url, headers=headers, data=payload, files=files)
                    res = r.content
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
            }, status=HTTP_400_BAD_REQUEST)


