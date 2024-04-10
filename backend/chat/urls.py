from django.urls import path
from .views import RoomView, RoomMessagesView, ChatView

urlpatterns = [
    path('list_conversation/', RoomView.as_view(), name='rooms'),
    path('room_messages/<str:room>/', RoomMessagesView.as_view(), name='room-messages'),
    path('chat/<str:username>/', ChatView.as_view(), name='chat'),
]