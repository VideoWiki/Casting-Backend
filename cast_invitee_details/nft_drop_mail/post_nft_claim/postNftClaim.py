from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ...models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist
from library.helper import user_info
from .postNftMailer import postCertiMailer
from api.global_variable import CLIENT_DOMAIN_URL


class postNftMail(APIView):
    def post(self, request):
        email = request.data["email"]
        nft_url = request.data["nft_url"]
        trans_id = request.data["transaction_id"]
        postCertiMailer(to_email=email, nft_url=nft_url, trans_id=trans_id)
        return Response({
            "status": True,
            "message": "mail sent successfully"
        })
