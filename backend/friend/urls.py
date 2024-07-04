from django.urls import path
from .views import FriendListView, FriendRequestListView, SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, BlockUserView, UnblockUserView, RemoveFriendView

# urls represent: 
# - list of friends
# - list of users that asked to be friends
# - send friend request
# - accept friend request
# - reject friend request
# - remove friend
# - block user
# - unblock user
urlpatterns = [
    path('friends-list/', FriendListView.as_view(), name='friends'),
    path('friend-requests/', FriendRequestListView.as_view(), name='friend-requests'),
    path('send-friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('accept-friend-request/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('reject-friend-request/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('remove-friend/', RemoveFriendView.as_view(), name='remove-friend'),
    path('block-user/', BlockUserView.as_view(), name='block-user'),
    path('unblock-user/', UnblockUserView.as_view(), name='unblock-user'),
]