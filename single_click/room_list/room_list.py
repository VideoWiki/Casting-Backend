from bbb_api.models import Meeting
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from library.helper import private_meeting_id_generator, \
    public_meeting_id_generator, generate_random_key, get_random_string
from bbb_api.create_event_api.views import timezone_adder
from bbb_api.create_event_email_sender import tc
import pytz, datetime
from api.global_variable import CLIENT_DOMAIN_URL
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from ..models import KeyDetails
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class get_rooms(APIView):
    permission_classes = [HasAPIKey]
    def get(self, request):
        username = request.GET.get("username")
        try:
            user_objs = Meeting.objects.filter(event_creator_name=username)
        except ObjectDoesNotExist:
            return Response({
                "message": "no cast found for this user",
                "status": HTTP_400_BAD_REQUEST
            })
        info_list = []
        for i in user_objs:
            data = {"event_name": i.event_name,
             "event_creator_name": i.event_creator_name,
             "public_meeting_id": i.public_meeting_id,
             "date": i.schedule_time.date(),
             "time": i.schedule_time.time(),
             "running": Meeting.is_meeting_running(i.private_meeting_id),
             "creator_url": {CLIENT_DOMAIN_URL + "/e/creator/join/{}/?pass={}".format(i.public_meeting_id,
                                                                                      i.hashed_moderator_password)},
             "participant_url": {CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(i.public_meeting_id,
                                                                             i.hashed_attendee_password)},
            "co-host_url": {CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(i.public_meeting_id, i.hashed_moderator_password)}
             }
            info_list.append(data)
        return Response({'status': True, 'meeting_info': info_list})
