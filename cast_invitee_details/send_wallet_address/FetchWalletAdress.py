from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from library.helper import user_info
from django.core.exceptions import ObjectDoesNotExist


class FetchWalletAdress(APIView):
    def get(self, request):
        public_cast_id = request.GET.get("cast_id")

        if public_cast_id == "":
            return Response({
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            meeting_obj = Meeting.objects.get(public_meeting_id=str(public_cast_id))
        except ObjectDoesNotExist:
            return Response({
                "message": "invalid cast_id"
            }, status=status.HTTP_400_BAD_REQUEST)
        meeting_user_id = meeting_obj.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass

        if curr_user_id == meeting_user_id:
            cast_invitee_obj = CastInviteeDetails.objects.filter(cast=meeting_obj)
            if cast_invitee_obj.exists():
                all_nft_enabled_obj = cast_invitee_obj.filter(nft_enable=True).all().exclude(metamask_address=None)
                wallet_address_list = [i.metamask_address for i in all_nft_enabled_obj]

        else:
            return Response({
                "message": "invalid user"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': True,
                         'wallet_address_list': wallet_address_list}
                        )
