from rest_framework.views import APIView
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework import status
from bbb_api.models import Meeting
from cast_invitee_details.models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist


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
                            name = item[0]
                            email = item[1]
                            role = item[2]
                            if name == "" or email == "" or role == "":
                                return Response({
                                    "status": False,
                                    "message": "invalid data"
                                },status= status.HTTP_400_BAD_REQUEST)
                            if CastInviteeDetails.objects.filter(cast=cast_obj, email=email).exists():
                                pass
                            else:
                                CastInviteeDetails.objects.create(cast=cast_obj,
                                                                  name=name,
                                                                  email=email,
                                                                  role=role,
                                                                  nft_enable=False)

        return Response({
            "status": True,
            "message": "successful"
        })
