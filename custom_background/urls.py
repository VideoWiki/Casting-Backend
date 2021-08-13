from .views import photo_api
from django.urls import path

urlpatterns = [
    path('photos/', photo_api.as_view()),
    ]

# path('post/photos/', post_pictures.as_view()),
#use above api to upload pictures manually.