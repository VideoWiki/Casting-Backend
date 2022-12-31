from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from ..models import MerkelTreeDetail
import ast

class FetchMerkelTreeDetails(APIView):
    def get(self, request):
        public_cast_id = request.GET.get("cast_id")

        if public_cast_id == "":
            return Response({
                "message": "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            meeting_obj = Meeting.objects.get(public_meeting_id=str(public_cast_id))
        except ObjectDoesNotExist:
            return Response({
                "message": "invalid cast_id"
            }, status=status.HTTP_400_BAD_REQUEST)
        data = MerkelTreeDetail.objects.get(cast=meeting_obj).data
        converted_data = ast.literal_eval(data)
        return Response({
            "status": True,
            "message": "successful",
            "data": converted_data
        })