from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist
from library.helper import user_info
from .nftMailer import nftMailer
from api.global_variable import CLIENT_DOMAIN_URL


class NftDropMail(APIView):
    def get(self, request):
        cast_id = request.GET.get("cast_id")
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
            invitee_obj = CastInviteeDetails.objects.filter(cast=cast_object, nft_enable=True).all()
            nft_drop_url = CLIENT_DOMAIN_URL + "/nftdrop/?cast_id={}".format(cast_object.public_meeting_id)
            for i in invitee_obj:
                if i.nft_mail_sent == False:
                    nftMailer(to_email=i.email, user_name=i.name, nft_drop_url=nft_drop_url)
                    i.nft_mail_sent = True
                    i.save()
                else:
                    pass
            return Response({
                "status": True,
                "message": "Successful"
            })
        else:
            return Response({
                "status": False,
                "message": "invalid user"
            }, status= status.HTTP_400_BAD_REQUEST)
