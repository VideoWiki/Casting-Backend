from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist
from library.helper import user_info


class UptadeInviteeDetails(APIView):
    def patch(self, request):
        invitee_details = request.data['invitee_list']
        cast_id = request.data['cast_id']
        try:
            cast_object = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
           return  Response({
               "status": False,
               "message": "cast does not exists"
           }, status= status.HTTP_400_BAD_REQUEST)
        user_id = cast_object.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass
        if curr_user_id == user_id:
            cast_invite_object = CastInviteeDetails.objects.filter(cast=cast_object)
            if len(invitee_details) > 0:
                for i in invitee_details:
                    id = i['id']
                    invitee_obj = cast_invite_object.get(id=id)
                    invitee_obj.email = i['email']
                    invitee_obj.role = i['type']
                    invitee_obj.nft_enable = i['nft_enable']
                    invitee_obj.save()
            else:
                return Response({
                    "status": False,
                    "message": "no existing invitee found"
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "status": True,
                "message": "updated"
            })
        else:
            return Response({
                "status": False,
                "message": "invalid user"
            }, status= status.HTTP_400_BAD_REQUEST)


