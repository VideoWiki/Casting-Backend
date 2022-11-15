from rest_framework.views import APIView
from bbb_api.models import Meeting
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from ..models import LearningAnalytics

class LearningAnalyticsView(APIView):
    def post(self, request):
        room_name = request.data["room_name"]
        creator_name = request.data["room_owner_name"]
        analytics_url = request.data["learning_analytics_url"]

        LearningAnalytics.objects.create(room_name=room_name, creator_name=creator_name, analytics_url=analytics_url)
        return Response({
            "status": True,
            "message": "successful"
        })