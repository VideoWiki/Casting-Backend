from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from rest_framework.permissions import AllowAny
from ..helper import send_otp_details
from django.core.exceptions import ObjectDoesNotExist
from ..views import send_otp
from django.contrib.auth.hashers import make_password


class SendOtp(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        cast_id = request.GET.get('cast_id')

        if cast_id == "" or email=="":
            return Response({
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)

        email_obj = CastInviteeDetails.objects.filter(cast=cast_obj)
        list_email = []

        for i in email_obj:
            list_email.append(i.email)

        if email in list_email:
            key = send_otp(email)

            if key:
                old = email_obj.filter(email__iexact=email)
                if old.exists():
                    old = old.first()
                    print(old)
                    count = old.count
                    # if count > 20:
                    #     return Response({
                    #         'status': False,
                    #         'detail' : 'Sending otp error. Limit Exceeded. Please contact customer support.'
                    #         })
                    old.count = count + 1
                    hashed_otp = make_password(key)
                    old.otp = hashed_otp
                    old.save()
                    print('Count Increase', count)
                    status_code = status.HTTP_200_OK
                    mail_status = send_otp_details(email, key)
                    return Response({
                        'message': 'otp sent successfully.',
                        'status': True,
                        'mail': mail_status}, status_code)
        else:
            return Response({
                "message": "invalid email"
            }, status=status.HTTP_400_BAD_REQUEST)
