from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist
from library.helper import user_info
from uuid import uuid4
import csv
from api.global_variable import BASE_DIR


class CsvDownloader(APIView):
    def get(self, request):
        cast_id = request.GET.get('cast_id')
        try:
            cast_object = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "cast does not exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        print(cast_object ,"ll")
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
                    otp_verified = i.verified,

                    wallet_address = i.metamask_address
                    otp_slice = str(otp_verified)[slice(2,-3)]
                    if otp_slice == 'True':
                        pass
                    else:
                        otp_slice = 'False'
                    d = {
                        "name": name,
                        "role": role,
                        "email": email,
                        "otp_verified": otp_slice,
                        "wallet_address": wallet_address
                    }
                    inv_list.append(d)
            random_name = str(uuid4())
            dir = BASE_DIR + "/cast_invitee_details/csv_downloader/csv_files/{}_invitee_list.csv".format(cast_object.event_name)
            print(dir)
            with open(dir, 'w', encoding='UTF8') as f:
                fieldnames = ['name', 'role', 'email', 'verified', 'wallet_address']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for i in inv_list:
                    print(i['otp_verified'])
                    writer.writerow({'name': i['name'], 'role': i['role'], 'email': i['email'], 'verified': i['otp_verified'], 'wallet_address': i['wallet_address']})
            f.close()
            return Response(
                {
                    "path": dir
                }
            )