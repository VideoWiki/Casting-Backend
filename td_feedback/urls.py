from django.urls import path
from .views import FeedbackAPIView
from .user_count import RoomAPIView

urlpatterns = [
    path('feedback/', FeedbackAPIView.as_view(), name='feedback-create'),
    path('user_count/', RoomAPIView.as_view(), name='feedback-create')

]
