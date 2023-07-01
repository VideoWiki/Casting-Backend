from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserCount
from datetime import datetime, timedelta



class RoomAPIView(APIView):
    def post(self, request):
        room_id = request.data.get('room_id')
        user_count = request.data.get('user_count')
        
        if room_id is None or user_count is None:
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)
        
        room = UserCount(room_id=room_id, user_count=user_count)
        room.save()
        
        return Response({'message': 'Room created successfully'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        room_id = request.query_params.get('room_id')
        
        if room_id is None:
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            rooms = UserCount.objects.filter(room_id=room_id)
        
        data = [{'room_id': room.room_id, 'user_count': room.user_count} for room in rooms]
        two_days_ago = datetime.now() - timedelta(days=1)
        old_feedbacks = UserCount.objects.filter(created_at__lt=two_days_ago)
        old_feedbacks.delete()
        
        return Response(data, status=status.HTTP_200_OK)
