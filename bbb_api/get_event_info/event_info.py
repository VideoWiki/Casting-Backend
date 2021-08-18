from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


class meeting_info(APIView):
    def get(self, request):
        public_meeting_id = request.GET.get('public_meeting_id')
        try:
            event_object = Meeting.objects.get(public_meeting_id= public_meeting_id)
            # result = Meeting.meeting_info(private_meeting_id_object.private_meeting_id, private_meeting_id_object.moderator_password)
            event_name = event_object.event_name
            event_creator_name = event_object.event_creator_name
            public_meeting_id = event_object.public_meeting_id
            description = event_object.short_description
            event_day = event_object.schedule_time.date()
            event_time = event_object.schedule_time.time()

            return Response({'status': True, 'meeting_info': {"event_name": event_name,
                                                              "event_creator_name": event_creator_name,
                                                              "public_meeting_id": public_meeting_id,
                                                              "description": description,
                                                              "date": event_day,
                                                              "time": event_time}})
        except ObjectDoesNotExist:
            return Response({"status": False,
                             "message": "meeting id does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)