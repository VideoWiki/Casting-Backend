import json
from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from bbb_api.join_event_api.join import event_scheduler, sub_time, add_time, time_in_range


class MagicUrlCreator(APIView):
    def post(self, request):
        cast_id = request.data['id']
        cast_key = request.data['pass']
        if cast_id == "":
            return Response({
                "message": "invalid cast id",
                "status": False
            }, status=HTTP_400_BAD_REQUEST)
        try:
            cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "message": "invalid cast id",
                "status": False
            },status=HTTP_400_BAD_REQUEST)
        if cast_obj.hashed_moderator_password == cast_key:
            pass
        else:
            return Response({
                "message": "invalid cast key",
                "status": False
            }, status=HTTP_400_BAD_REQUEST)
        duration = cast_obj.duration
        if duration == 0:
            duration = 1440
        subtracted_time = sub_time(cast_obj.schedule_time)
        added_time = add_time(cast_obj.schedule_time, duration)
        current = datetime.utcnow()
        status = time_in_range(subtracted_time, added_time, current)
        name = cast_obj.event_creator_name
        if "@" in name:
            split_name = name.split("@")
            name = split_name[0]
        else:
            pass
        if status == True:
            event_scheduler(cast_obj.private_meeting_id)
            result = Meeting.join_url(cast_obj.private_meeting_id,
                                      name,
                                      cast_obj.moderator_password,
                                      force_listen_only=False,
                                      enable_screen_sharing=True,
                                      enable_webcam=True
                                      )
            return Response({
                "status": "true",
                "cast_url": result
            })
        else:
            return Response({"status": False,
                             "message": "please check the scheduled cast start time"},
                            status=HTTP_400_BAD_REQUEST
                            )

