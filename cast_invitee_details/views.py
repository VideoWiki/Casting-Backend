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
# Create your views here.

class add_invitees(APIView):
    def post(self, request):
        cast_id = request.data["cast_id"]
        obj = Meeting.objects.get(public_meeting_id=cast_id)
        if id != None:
            CastInviteeDetails.cast_id = cast_id
            invitee_list = request.data['invitee_list']
            for i in invitee_list:
                CastInviteeDetails.objects.create(cast=obj, name=i["name"], email=i["email"], role=i["type"])
            return Response({"status": True})
        return Response({"status": False})


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
        if curr_user_id == user_id:
            cast_invite_object = CastInviteeDetails.objects.filter(cast=cast_object)
            inv_list = []
            if cast_invite_object.count() != 0:
                for i in cast_invite_object:
                    name = i.name
                    role = i.role
                    email = i.email
                    d = {
                        "name": name,
                        "role": role,
                        "email": email
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
    def get(self, request):
        cast_id = request.GET.get('cast_id')
        email = request.GET.get('email')
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
                for i in cast_invite_object:
                    if i.email == email:
                        i.delete()
                        return Response({
                            "status": True,
                            "message": "invitee deleted successfully"
                        })
                else:
                    return Response({
                        "status": False,
                        "message": "email not found"
                    }, status=status.HTTP_400_BAD_REQUEST)
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



class validate_email_Send_otp(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        cast_id = request.GET.get('cast_id')
        if email:
            email  = str(email)
            try:
                meet_obj = Meeting.objects.get(public_meeting_id = cast_id)
            except ObjectDoesNotExist:
                message = "cast id does not exist"
                return Response({"status": False,
                                 "message": message}, status=status.HTTP_400_BAD_REQUEST)
            cast_obj = CastInviteeDetails.objects.filter(cast=meet_obj)
            email_o = cast_obj.filter(email=str(email)).all()
            if email_o.count() != 0:
                for i in email_o:
                    e_role = i.role
                    if e_role == "viewer":
                            key = send_otp(email)
                            if key:
                                old = email_o.filter(email__iexact=email)
                                if old.exists():
                                    old = old.first()
                                    count = old.count
                                    old.count = count + 1
                                    old.otp = key
                                    old.save()
                                    status_code = status.HTTP_200_OK
                                    mail_status = send_otp_details(email, key)
                                    return Response({
                                        'status': True,
                                        'detail': 'otp sent successfully.',
                                        'mail': mail_status
                                    }, status_code)
                    else:
                        message = "user permission error"
                        return Response({"status": False,
                                         "message": message}, status=status.HTTP_400_BAD_REQUEST)
            elif email_o.count() == 0:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response({
                    'status': False,
                    'detail': 'invalid email'
                }, status_code)

        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({
                'status' : False,
                'detail' : 'please provide email'
                }, status_code)


def send_otp(email):
    if email:
        key = get_random_string(6, '0123456789')
        return key
    else:
        return False


class validate_otp(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email' , False)
        otp_sent = request.GET.get('otp', False)
        cast_id = request.GET.get('cast_id')
        meet_obj = Meeting.objects.get(public_meeting_id=cast_id)
        cast_obj = CastInviteeDetails.objects.filter(cast=meet_obj)
        email_o = cast_obj.filter(email=str(email)).all()
        if email and otp_sent:
            old = email_o.filter(email__iexact = email)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    response = "validated"
                    status_code = status.HTTP_200_OK
                    return Response({"status": True,
                                     "message":response}, status_code)

                else:
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response({
                        'status' : False,
                        'detail' : 'otp incorrect.'
                        }, status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response({
                    'status' : False,
                    'detail' : 'invalid email'
                    }, status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({
                'status' : False,
                'detail' : 'email and otp is required'
                }, status_code)







