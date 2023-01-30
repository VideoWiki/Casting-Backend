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
from ..models import KeyDetails, CustomRoomInfo
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


class get_all_rooms(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        username = request.GET.get("username")

        info_list = []
        custom_room_list = []
        simple_room_list = []
        room_obj = CustomRoomInfo.objects.filter(username= username)
        if len(room_obj) > 0:
            for i in room_obj:
                if i.room_type == "simple":
                    data = {"event_name": i.cast.event_name,
                                    "event_creator_name": i.cast.event_creator_name,
                                    "public_meeting_id": i.cast.public_meeting_id,
                                    "date": i.cast.schedule_time.date(),
                                    "time": i.cast.schedule_time.time(),
                                    "running": Meeting.is_meeting_running(i.cast.private_meeting_id),
                                    "creator_url": {CLIENT_DOMAIN_URL + "/e/creator/join/{}/?pass={}".format(i.cast.public_meeting_id,
                                                                                                             i.cast.hashed_moderator_password)},
                                    "participant_url": {CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(i.cast.public_meeting_id,
                                                                                                    i.cast.hashed_attendee_password)},
                                    "co-host_url": {
                                        CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(i.cast.public_meeting_id,
                                                                                    i.cast.hashed_moderator_password)}
                                    }
                    simple_room_list.append(data)
                elif i.room_type == "custom":
                    data = {"event_name": i.cast.event_name,
                            "event_creator_name": i.cast.event_creator_name,
                            "public_meeting_id": i.cast.public_meeting_id,
                            "date": i.cast.schedule_time.date(),
                            "time": i.cast.schedule_time.time(),
                            "running": Meeting.is_meeting_running(i.cast.private_meeting_id),
                            "creator_url": {CLIENT_DOMAIN_URL + "/e/creator/join/{}/?pass={}".format(
                                i.cast.public_meeting_id,
                                i.cast.hashed_moderator_password)},
                            "participant_url": {
                                CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(i.cast.public_meeting_id,
                                                                            i.cast.hashed_attendee_password)},
                            "co-host_url": {
                                CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(i.cast.public_meeting_id,
                                                                            i.cast.hashed_moderator_password)}
                            }
                    custom_room_list.append(data)

        simple_data = {"room_list":simple_room_list}
        custom_data = {"room_list":custom_room_list}
        return Response({'status': True, "simple_data": simple_data, "custom_data":custom_data})
