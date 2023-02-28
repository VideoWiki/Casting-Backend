from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from .models import CastInviteeDetails
from rest_framework.permissions import AllowAny
from django.utils.crypto import get_random_string
from .helper import send_otp_details
from django.core.exceptions import ObjectDoesNotExist
from library.helper import user_info
from django.core.signing import Signer
# Create your views here.


class add_invitees(APIView):
    def post(self, request):
        cast_id = request.data["cast_id"]
        obj = Meeting.objects.get(public_meeting_id=cast_id)
        user_id = obj.user_id
        curr_user_id = -1
        added_invitees_list = []
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass
        if curr_user_id == user_id:
            if cast_id != None:
                CastInviteeDetails.cast_id = cast_id
                invitee_list = request.data['invitee_list']
                for i in invitee_list:
                    if i["give_nft"] == "True":
                        bool_nft_enable = True
                    else:
                        bool_nft_enable = False
                    CastInviteeDetails.objects.create(cast=obj,
                                                      email=i["email"].lower(),
                                                      role=i["type"],
                                                      nft_enable=bool_nft_enable,
                                                      invited= True,
                                                      mint='not started'
                                                      )
                    if CastInviteeDetails.objects.filter(cast=obj, email=i["email"].lower()).exists():
                        inv_obj = CastInviteeDetails.objects.filter(cast=obj, email=i["email"].lower()).get()
                        d = {
                            "id": inv_obj.id,
                            "role": inv_obj.role,
                            "email": inv_obj.email,
                            "otp_verified": inv_obj.verified,
                            "wallet_address": inv_obj.metamask_address,
                            "nft_enable": inv_obj.nft_enable
                        }
                        added_invitees_list.append(d)
                    else:
                        pass
                return Response({
                    "status": True,
                    "data": added_invitees_list
                })
        else:
            return Response({
                "status": False,
                "message": "unauthorised user"
            })


class fetch_details(APIView):
    def get(self, request):
        cast_id = request.GET.get('cast_id')
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
        res = ""
        if curr_user_id == user_id:
            cast_invite_object = CastInviteeDetails.objects.filter(cast=cast_object)
            inv_list = []
            if cast_invite_object.count() != 0:
                for i in cast_invite_object:
                    id = i.id
                    role = i.role
                    email = i.email
                    otp_verified = i.verified,
                    wallet_address = str(i.metamask_address),
                    if wallet_address[0] != "None":
                        test_list = [0, 1, 2, 3, 38, 39, 40, 41]
                        repl_char = '*'
                        signer = Signer()
                        unhashed_wallet_add = signer.unsign(wallet_address[0])
                        res = unhashed_wallet_add
                    else:
                        if wallet_address[0] == "None":
                            res = ""
                    nft_enable = i.nft_enable
                    vc_enable = i.vc_enable
                    mint_status = i.mint
                    vc_mint_status = i.vc_mint
                    joined = i.joined
                    d = {
                        "id": id,
                        "role": role,
                        "email": email,
                        "otp_verified": otp_verified,
                        "wallet_address": res,
                        "nft_enable": nft_enable,
                        "vc_enable": vc_enable,
                        "mint_status": mint_status,
                        "vc_mint_status": vc_mint_status,
                        "joined": joined
                    }
                    inv_list.append(d)
                return Response({
                    "status": True,
                    "data": inv_list
                    })
            else:
                return Response({
                    "status": False,
                    "message": "no invitee found"
                })

        else:
            return Response({
                "status": False,
                "message": "user permission error"
            }, status= status.HTTP_400_BAD_REQUEST)



class delete_invitee(APIView):
    def delete(self, request):
        cast_id = request.data['cast_id']
        email = request.data['email']

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
            cast_invite_object = CastInviteeDetails.objects.filter(cast=cast_object)
            if cast_invite_object.count() != 0:
                for i in email:
                    if not (i is None):

                        
                        CastInviteeDetails.objects.get(cast=cast_object, email=i).delete()
                return Response({
                            "status": True,
                            "message": "invitee deleted successfully"
                        })


                        


            else:
                return Response({
                        "status": False,
                        "message": "no invitee found"
                    }, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({
                    "status": False,
                    "message": "user permission error"
                    }, status=status.HTTP_400_BAD_REQUEST)


def send_otp(email):
    if email:
        key = get_random_string(6, '0123456789')
        return key
    else:
        return False










