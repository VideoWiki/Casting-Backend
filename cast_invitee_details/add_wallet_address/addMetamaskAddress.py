from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from django.core.signing import Signer
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class AddUser(APIView):
    def post(self, request):
        public_address = request.data["public_address"]
        public_cast_id = request.data["cast_id"]
        email = request.data["email"]
        email = email.lower()
        if public_address == "" or public_cast_id == "" or email=="":
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
            email_obj = obj.get(email__exact=email)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid email"
            }, status=status.HTTP_400_BAD_REQUEST)
        if email_obj.mint_count == 1:
            return Response({
                "status": False,
                "message": "can't update wallet address after mint"
            }, status=status.HTTP_400_BAD_REQUEST)
        if email_obj.verified != 'True':
            return Response({
                "status": False,
                "message": "email not verified"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            pass
        try:
            email_obj.metamask_address = hashed_wallet_add
            email_obj.save()
        except IntegrityError:
            return Response({
                "status": False,
                "message": "wallet address already linked"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "status": True,
            "message": "successful"
        })