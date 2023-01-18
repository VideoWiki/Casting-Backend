from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import MerkelTreeDetail
from django.core.exceptions import ObjectDoesNotExist
import json
import ast

class PostMerkelTreeDetails(APIView):
    def post(self, request):
        public_cast_id = request.data["cast_id"]
        merkel_data = request.data["data"]

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
        if not MerkelTreeDetail.objects.filter(cast=meeting_obj).exists():
            MerkelTreeDetail.objects.create(cast=meeting_obj, data=merkel_data)
        else:
            merkel_obj = MerkelTreeDetail.objects.get(cast=meeting_obj)
            # existing_data = merkel_obj.data
            # converted_dict = ast.literal_eval(existing_data)
            # converted_dict.update(merkel_data)
            # merkel_obj.data = converted_dict
            # merkel_obj.save()
            merkel_obj.data = merkel_data
            merkel_obj.save()
        return Response({
            "status": True,
            "message": "successful"
        })

