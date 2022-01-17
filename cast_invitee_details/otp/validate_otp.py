from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password


class ValidateOtp(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email' , False)
        otp_sent = request.GET.get('otp', False)
        cast_id = request.GET.get('cast_id')

        meet_obj = Meeting.objects.get(public_meeting_id=cast_id)
        cast_obj = CastInviteeDetails.objects.filter(cast=meet_obj)

        if email and otp_sent:
            old = cast_obj.filter(email__iexact = email)
            if old.exists():
                old = old.first()
                otp = old.otp
                if check_password(otp_sent, otp):
                    old.verified = True
                    old.save()
                    response = "validated"
                    status_code = status.HTTP_200_OK
                    return Response({"status": True,
                                     "message": response}, status_code)
                else:
                    status_code = status.HTTP_400_BAD_REQUEST
                return Response({
                    'status': False,
                    'detail': 'otp incorrect.'
                }, status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response({
                    'status': False,
                    'detail': 'first proceed via sending otp request.'
                }, status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({
                'status': False,
                'detail': 'please provide both email and otp for validations'
            }, status_code)