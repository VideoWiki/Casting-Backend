from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from rest_framework import status
from ..models import MerkelTreeDetail
from django.core.exceptions import ObjectDoesNotExist


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

        MerkelTreeDetail.objects.create(cast=meeting_obj, data=merkel_data)
        return Response({
            "status": True,
            "message": "successful"
        })

