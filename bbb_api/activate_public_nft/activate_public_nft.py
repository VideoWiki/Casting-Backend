from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from library.helper import user_info
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


class NftActivatePublic(APIView):
    def post(self, request):
        cast_id = request.data["cast_id"]
        nft_activate_value = request.data["nft_activate"]
        try:
            meeting_obj = Meeting.objects.get(public_meeting_id=str(cast_id))
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid cast id"
            }, status=status.HTTP_400_BAD_REQUEST)
        meeting_user_id = meeting_obj.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass
        if curr_user_id == meeting_user_id:
            if nft_activate_value == 'True':
                meeting_obj.public_nft_activate = True
                meeting_obj.save(update_fields=['public_nft_activate'])
                message = "NFT activated"
            elif nft_activate_value == 'False':
                meeting_obj.public_nft_activate = False
                meeting_obj.save(update_fields=['public_nft_activate'])
                message = "NFT deactivated"
        return Response({"status": True,
                         "message": message
                         })