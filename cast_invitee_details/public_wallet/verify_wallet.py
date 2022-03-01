from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import PublicWallet
from django.core.signing import Signer
from django.core.exceptions import ObjectDoesNotExist


class PublicWalletVerify(APIView):
    def get(self, request):
        public_address = request.GET.get("public_address")
        public_cast_id = request.GET.get("cast_id")
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
        print(cast_obj)
        try:
            wallet_obj = PublicWallet.objects.filter(cast=cast_obj, metamask_address=hashed_wallet_add)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid wallet address"
            }, status=status.HTTP_400_BAD_REQUEST)
        if wallet_obj.exists():
            if wallet_obj.get().mint_count >= 1:
                return Response({
                    "status": False,
                    "message": "NFT already minted"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                m_wallet_obj = wallet_obj.get()
                m_wallet_obj.metamask_verified = True
                m_wallet_obj.save()
        else:
            return Response({
                "status": False,
                "message": "invalid wallet address"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "status": True,
            "message": "successful"
        })