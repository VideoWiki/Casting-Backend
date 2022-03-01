from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from django.core.signing import Signer


class VerifyWalletAddress(APIView):
    def get(self, request):
        cast_id = request.GET.get("cast_id")
        public_address = request.GET.get("public_address")

        if public_address == "" or cast_id == "":
            return Response({
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)
        signer = Signer()
        signed_add = signer.sign(public_address)
        cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        try:
            saved_pub_add = CastInviteeDetails.objects.filter(cast=cast_obj, metamask_address=signed_add).all()[0]
            if saved_pub_add.nft_enable == False:
                return Response({
                    "status": False,
                    "message": "NFT not enabled for this user"
                }, status= status.HTTP_400_BAD_REQUEST)
            else:
                pass
            if saved_pub_add.mint_count >= 1:
                return Response({
                    "status": False,
                    "message": "NFT already claimed"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
            saved_pub_add.metamask_verified = True
            saved_pub_add.save()
            return Response({
                "status": True,
                "public_address_verified": True
            })
        except IndexError:
            return Response({
                "status": False,
                "public_address_verified": False
            }, status=status.HTTP_400_BAD_REQUEST)
