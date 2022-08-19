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
# Create your views here.


class create_cast(APIView):
    def post(self, request):
        meeting = Meeting()
        event_name = request.data['event_name']
        name = request.data['creator_name']
        if event_name == "" or name == "":
            return Response({
                "status": False,
                "message": "cast name or creator name can't be empty"
            }, status=HTTP_400_BAD_REQUEST)
        meeting.event_name = event_name
        meeting.event_creator_name = name
        meeting.private_meeting_id = private_meeting_id_generator()
        meeting.public_meeting_id = public_meeting_id_generator()
        meeting.meeting_type = "public"
        meeting.attendee_password = generate_random_key()
        meeting.hashed_attendee_password = get_random_string()
        meeting.moderator_password = generate_random_key()
        meeting.hashed_moderator_password = get_random_string()
        logo = "https://class.video.wiki/images/VideoWiki_Logo.svg"
        meeting.logo = logo
        schedule_time = request.data['schedule_time']
        timezone = request.data['timezone']
        if timezone == "":
            return Response({
                "status": False,
                "message": "invalid timezone"}, status=HTTP_400_BAD_REQUEST)
        timezone_adder(tz=timezone)
        meeting.raw_time = schedule_time + "~" + timezone
        ct = tc(schedule_time, timezone)
        time_now = datetime.datetime.now().astimezone(pytz.utc)
        if time_now > ct:
            return Response({
                "status": False,
                "message": "invalid schedule time"}, status=HTTP_400_BAD_REQUEST)
        meeting.schedule_time = ct
        meeting.primary_color = "#753FB5"
        meeting.record = True
        meeting.user_id = 0
        meeting.save()
        event_creator_url = {CLIENT_DOMAIN_URL + "/e/creator/join/{}/?pass={}".format(meeting.public_meeting_id, meeting.hashed_moderator_password)}
        participant_url = {CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(meeting.public_meeting_id, meeting.hashed_attendee_password)}
        co_host_url = {CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(meeting.public_meeting_id, meeting.hashed_moderator_password)}
        return Response({
            "status": True,
            "cast_name": event_name,
            "public_cast_id": meeting.public_meeting_id,
            "message": "cast_created_successfully",
            "creator_url": event_creator_url,
            "participant_url": participant_url,
            "co-host_url": co_host_url
        })

