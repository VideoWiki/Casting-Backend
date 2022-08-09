from rest_framework.views import APIView
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework import status
from bbb_api.models import Meeting
from cast_invitee_details.models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist
from library.helper import user_info


class ParseExcel(APIView):
    def post(self, request):
        try:
            excel_file = request.FILES['file']
            cast_id = request.data["cast_id"]
        except MultiValueDictKeyError:
            return Response({"status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid cast id"
            }, status=status.HTTP_400_BAD_REQUEST)
        meeting_user_id = cast_obj.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass
        if curr_user_id == meeting_user_id:
            if (str(excel_file).split(".")[-1] == "xls"):
                data = xls_get(excel_file, column_limit=4)
            elif (str(excel_file).split(".")[-1] == "xlsx"):
                data = xlsx_get(excel_file, column_limit=4)
            else:
                return Response({
                    "status": False,
                    "message": "invalid file type"
                }, status=status.HTTP_400_BAD_REQUEST)
            for i in data:
                attendees  = data[i]
                if len(attendees) > 1:
                    for item in attendees:
                        if len(item) < 3:
                            return Response({
                                "status": False,
                                "message": "invalid data"
                            }, status=status.HTTP_400_BAD_REQUEST)
                        if (len(item) > 0):
                            if (item[0] != "Name"):
                                email = item[1]
                                role = item[2]
                                if email == "" or role == "":
                                    return Response({
                                        "status": False,
                                        "message": "invalid data"
                                    },status= status.HTTP_400_BAD_REQUEST)
                                if CastInviteeDetails.objects.filter(cast=cast_obj, email=email.lower()).exists():
                                    pass
                                else:
                                    CastInviteeDetails.objects.create(cast=cast_obj,
                                                                      email=email.lower(),
                                                                      role=role.lower(),
                                                                      nft_enable=False)
        else:
            return Response({
                "message": "invalid user",
                "status": False
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "successful"
        })
