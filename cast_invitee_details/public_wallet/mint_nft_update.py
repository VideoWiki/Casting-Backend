from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails, PublicWallet
from django.core.signing import Signer


class PublicMintUpdate(APIView):
    def patch(self, request):
        cast_id = request.data['cast_id']
        public_address = request.data['public_address']
        transaction_id = request.data['mint_id']
        mint_status = request.data['status']

        if public_address == "" or cast_id == "":
            return Response({
                "status": False,
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)
        signer = Signer()
        hashed_pub_add = signer.sign(public_address)
        cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        try:
            obj = PublicWallet.objects.filter(cast=cast_obj, metamask_address=hashed_pub_add).all()[0]
        except IndexError:
            return Response({
                "status": False,
                "message": "invalid address"
            }, status=status.HTTP_400_BAD_REQUEST)
        if obj.metamask_verified != 'True':
            return Response({
                "status": False,
                "message": "invalid public adrdess"
            }, status=status.HTTP_400_BAD_REQUEST)
        if mint_status == "successful":
            if obj.mint_count == 0:
                if transaction_id == "":
                    return Response({
                        "status": False,
                        "message": "no transaction id"
                    }, status=status.HTTP_400_BAD_REQUEST)
                obj.transaction_id = transaction_id
                obj.mint = mint_status
                obj.mint_count = 1
                obj.save()
            else:
                return Response({
                    "status": False,
                    "message": "already minted"
                }, status= status.HTTP_400_BAD_REQUEST)
        elif mint_status == "started":
            if obj.mint_count == 0:
                obj.transaction_id = transaction_id
                obj.mint = mint_status
                obj.mint_count = 0
                obj.save()
        else:
            return Response({
                "status": False,
                "message": "already minted"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "status": True,
            "message": "successful"
        })



