from django.urls import path
from add_text_to_image.views import textAdderView
urlpatterns = [
    path('add/text/image/', textAdderView.as_view()),
]