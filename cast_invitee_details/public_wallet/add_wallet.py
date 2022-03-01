from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails, PublicWallet
from django.core.signing import Signer
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class PublicWalletAdd(APIView):
    def post(self, request):
        public_address = request.data["public_address"]
        public_cast_id = request.data["cast_id"]
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
        try:
            PublicWallet.objects.create(cast=cast_obj, metamask_address=hashed_wallet_add, mint_count=0)
        except IntegrityError:
            return Response({
                "status": False,
                "message": "wallet address already linked"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "status": True,
            "message": "successful"
        })