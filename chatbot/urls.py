from .views import chatbot_view
from django.urls import path

urlpatterns = [
    path('chat/', chatbot_view, name='chatbot'),
    ]