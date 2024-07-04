from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Friend, FriendRequest, Block
from .serializers import FriendSerializer, FriendRequestSerializer, BlockSerializer
from users.models import Account

#list of friends
class FriendListView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user)

#list of users that are not friends yet and that are not blocked by the user
class FriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        blocked_users = Block.objects.filter(user=self.request.user).values_list('blocked_user', flat=True)
        return FriendRequest.objects.filter(to_user=self.request.user).exclude(from_user__in=blocked_users)

#send friend request
class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        target = request.data['username']
        try :
            target = Account.objects.get(username=target)
        except:
            return Response({'error': 'User not found'}, status=404)
        #check if the user target is blocked by the user
        if Block.objects.filter(user=request.user, blocked_user=target).exists():
            return Response({'error': 'You have blocked this user'}, status=400)
        #check if the user is blocked by the user target
        if Block.objects.filter(user=target, blocked_user=request.user).exists():
            return Response({'error': 'You are blocked by this user'}, status=400)
        #check if they are already friends
        if Friend.objects.filter(user=request.user, friend=target).exists():
            return Response({'error': 'You are already friends'}, status=400)
        #check if a friend request has already been sent
        if FriendRequest.objects.filter(from_user=request.user, to_user=target).exists():
            return Response({'error': 'A friend request has already been sent'}, status=400)
        #check if the user target has already sent a friend request
        if FriendRequest.objects.filter(from_user=target, to_user=request.user).exists():
            # Accept the friend request
            friend_request = FriendRequest.objects.get(from_user=target, to_user=request.user)
            Friend.objects.create(user=friend_request.to_user, friend=friend_request.from_user)
            Friend.objects.create(user=friend_request.from_user, friend=friend_request.to_user)
            friend_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.create(request, target)

    def create(self, request, target):
        FriendRequest.objects.create(from_user=request.user, to_user=target)
        return Response(status=status.HTTP_201_CREATED)

# when the user accepts a friend request
class AcceptFriendRequestView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            friend_request = self.get_object(request, *args, **kwargs)
            Friend.objects.create(user=friend_request.to_user, friend=friend_request.from_user)
            Friend.objects.create(user=friend_request.from_user, friend=friend_request.to_user)
            friend_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'Friend request not found'}, status=404)

    def get_object(self, request, *args, **kwargs):
        target = Account.objects.get(username=request.data['username'])
        return FriendRequest.objects.get(from_user=target, to_user=request.user)

# when the user rejects a friend request
class RejectFriendRequestView(generics.DestroyAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            friend_request = self.get_object(request, *args, **kwargs)
            friend_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'Friend request not found'}, status=404)

    def get_object(self, request, *args, **kwargs):
        target = Account.objects.get(username=request.data['username'])
        return FriendRequest.objects.get(from_user=target, to_user=request.user)
    
#remove a friend
class RemoveFriendView(generics.DestroyAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            target = Account.objects.get(username=request.data['username'])
            relation = Friend.objects.get(user=request.user, friend=target)
            relation.delete()
            relation = Friend.objects.get(user=target, friend=request.user)
            relation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'Friend not found'}, status=404)

# when the user blocks another user
class BlockUserView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        to_block = request.data['username']
        try:
            to_block = Account.objects.get(username=to_block)
        except:
            return Response({'error': 'User not found'}, status=404)
        
        if request.user == to_block:
            return Response({'error': 'You cannot block yourself'}, status=400)
        if Block.objects.filter(user=request.user, blocked_user=to_block).exists():
            return Response({'error': 'You have already blocked this user'}, status=400)
        #check if they are already friendsso dont block them
        if Friend.objects.filter(user=request.user, friend=to_block).exists():
            return Response({'error': "Can't block a friend"}, status=400)
        #check if a friend request has already been sent if so remove it
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_block).exists():
            FriendRequest.objects.filter(from_user=request.user, to_user=to_block).delete()
        #check if the user target has already sent a friend request if so remove it
        if FriendRequest.objects.filter(from_user=to_block, to_user=request.user).exists():
            FriendRequest.objects.filter(from_user=to_block, to_user=request.user).delete()
        return self.block_user(request, to_block)
    
    def block_user(self, request, to_block):
        Block.objects.create(user=request.user, blocked_user=to_block)
        return Response(status=status.HTTP_201_CREATED)

# when the user unblocks another user
class UnblockUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlockSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            block = self.get_object(request, *args, **kwargs)
            block.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'Block not found'}, status=404)

    def get_object(self, request, *args, **kwargs):
        target = Account.objects.get(username=request.data['username'])
        return Block.objects.get(user=request.user, blocked_user=target)