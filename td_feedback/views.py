# feedback/views.py

from rest_framework.views import APIView
from .models import Feedback
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta


class FeedbackAPIView(APIView):
    def post(self, request):
        sender = request.data.get('sender')
        receiver = request.data.get('receiver')
        room_id = request.data.get('room_id')
        feedback_text = request.data.get('feedback_text')

        # Check if the feedback already exists for the given room_id
        # if Feedback.objects.filter(room_id=room_id).exists():
        #     return Response({'error': 'Feedback already exists for this room_id'}, status=status.HTTP_400_BAD_REQUEST)

        feedback = Feedback(sender=sender, receiver=receiver, room_id=room_id, feedback_text=feedback_text)
        feedback.save()

        return Response({'message': 'Feedback stored successfully'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        room_id = request.query_params.get('room_id')
        print(room_id)
        if not room_id:
            return Response({'error': 'Missing room_id parameter'}, status=status.HTTP_400_BAD_REQUEST)

        feedbacks = Feedback.objects.filter(room_id=room_id)
        serialized_feedbacks = []
        for feedback in feedbacks:
            serialized_feedbacks.append({
                'sender': feedback.sender,
                'receiver': feedback.receiver,
                'room_id': feedback.room_id,
                'feedback_text': feedback.feedback_text,
                'created_at': feedback.created_at
            })

        two_days_ago = datetime.now() - timedelta(days=1)
        old_feedbacks = Feedback.objects.filter(created_at__lt=two_days_ago)
        old_feedbacks.delete()

        return Response(serialized_feedbacks, status=status.HTTP_200_OK)

    def delete(self, request):
        room_id = request.data.get('room_id')

        if not room_id:
            return Response({'error': 'Missing room_id parameter'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the feedback exists for the given room_id
        feedbacks = Feedback.objects.filter(room_id=room_id)
        if not feedbacks.exists():
            return Response({'error': 'No feedback found for this room_id'}, status=status.HTTP_404_NOT_FOUND)

        feedbacks.delete()

        return Response({'message': 'Feedback deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
