from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from django.core.signing import Signer
from django.core.exceptions import ObjectDoesNotExist

class SendHashedId(APIView):
    def get(self, request):
        public_address = request.GET.get("public_address")
        public_cast_id = request.GET.get("cast_id")
        nft_type = request.GET.get("nft_type")
        if public_address == "" or public_cast_id == "":
            return Response({
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)
        signer = Signer()
        hashed_wallet_add = signer.sign(public_address)
        try:
            cast_obj = Meeting.objects.get(public_meeting_id=public_cast_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid cast id"
            }, status=status.HTTP_400_BAD_REQUEST)
        obj = CastInviteeDetails.objects.filter(cast= cast_obj).all()
        try:
            hashed_metamask_obj = obj.get(metamask_address=hashed_wallet_add)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid public address"
            }, status=status.HTTP_400_BAD_REQUEST)
        if nft_type == "vc":
            print("vc")
            if hashed_metamask_obj.vc_mint_count == 1:
                statu_s = True
                trans_id = hashed_metamask_obj.vc_transaction_id
                status_code = status.HTTP_200_OK
            else:
                statu_s = False
                trans_id = "not available"
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            if hashed_metamask_obj.mint_count == 1:
                statu_s = True
                trans_id = hashed_metamask_obj.transaction_id
                status_code = status.HTTP_200_OK
            else:
                statu_s = False
                trans_id = "not available"
                status_code = status.HTTP_400_BAD_REQUEST

        return Response({
            "status": statu_s,
            "hashed_id": trans_id
        }, status= status_code)