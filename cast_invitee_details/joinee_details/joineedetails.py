from rest_framework.views import APIView
from ..models import CastJoineeDetails
from rest_framework import status
from bbb_api.models import Meeting
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from api.global_variable import BASE_URL


class JoineeDetails(APIView):
    def post(self, request):
        cast_id = request.data["cast_id"]
        name = request.data["name"]
        # avatar = request.data["avatar"]
        try:
            cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid cast id"
            }, status=status.HTTP_400_BAD_REQUEST)
        cast_event_id = cast_obj.id
        CastJoineeDetails.objects.create(cast_id=cast_event_id, name= name)
        return Response({
            "status": True,
            "message": "successful"
        })


class FetchJoineeDetails(APIView):
    def get(self, request):
        cast_id = request.GET.get("cast_id")
        try:
            cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid cast id"
            }, status=status.HTTP_400_BAD_REQUEST)
        cast_event_id = cast_obj.id
        joinee_obj = CastJoineeDetails.objects.filter(cast_id=cast_event_id)
        joinee_list = []
        if joinee_obj.count() != 0:
            for i in joinee_obj:
                name = i.name
                # try:
                #     avatar = i.avatar.url
                #     avatar = BASE_URL + avatar
                # except ValueError:
                #     avatar = None
                joinee_dict = {"name": name,
                               # "avatar": avatar
                               }
                joinee_list.append(joinee_dict)
            return Response({
                "status": True,
                "data": joinee_list
            })
        else:
            return Response({
                "status": False,
                "message": "no joinee found"
            })




