from django.urls import path
from .views import SaveClassDetails, GetClassDetails

urlpatterns = [
    path('class/joinee/details/', SaveClassDetails.as_view()),
    path('get/class/joinee/details/', GetClassDetails.as_view()),
    ]