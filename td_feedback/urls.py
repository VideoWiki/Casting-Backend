from django.urls import path
from .views import FeedbackAPIView

urlpatterns = [
    path('feedback/', FeedbackAPIView.as_view(), name='feedback-create'),

]