from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
from cast_invitee_details.models import CastInviteeDetails
from api.global_variable import CLIENT_DOMAIN_URL


class get_invitee_details(APIView):
    def get(self, request):
        cast_id = request.GET.get('cast_id')
        try:
            cast_object = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
           return  Response({
               "status": False,
               "message": "cast does not exists"
           }, status= status.HTTP_400_BAD_REQUEST)
        meeting_type = cast_object.meeting_type
        cast_invite_object = CastInviteeDetails.objects.filter(cast=cast_object)
        inv_list = []
        inv_list.append({"email":str(cast_object.event_creator_email),
                         "cast_url": CLIENT_DOMAIN_URL+"/mycasts"})
        if cast_invite_object.count() != 0:
            if meeting_type == "private":
                for i in cast_invite_object:
                    email = i.email
                    cast_url = CLIENT_DOMAIN_URL + "/e/{}/".format(cast_object.public_meeting_id) + "?email={}".format(email)
                    item_d= {"email" : email,
                             "cast_url": cast_url}
                    inv_list.append(item_d)

            if meeting_type == "public":
                for i in cast_invite_object:
                    email = i.email
                    role = i.role
                    if role == "moderator":
                        pass_key = cast_object.hashed_moderator_password
                    if role == "participant":
                        pass_key = cast_object.hashed_attendee_password
                    if role == "viewer":
                        pass_key = cast_object.hashed_viewer_password

                    cast_url = CLIENT_DOMAIN_URL + "/e/{}/".format(cast_object.public_meeting_id) + "?pass={}".format(pass_key)
                    item_d = {"email": email,
                              "cast_url": cast_url}
                    inv_list.append(item_d)
        return Response({"status": True,
                         "event_name": cast_object.event_name,
                         "event_creator_name": cast_object.event_creator_name,
                         "public_meeting_id": cast_object.public_meeting_id,
                         "date": cast_object.schedule_time.date(),
                         "time": cast_object.schedule_time.time(),
                         "cast_running_status": Meeting.is_meeting_running(cast_object.private_meeting_id),
                         "data": inv_list})
