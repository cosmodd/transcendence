from django.db import models
from users.models import Account

class Friend(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f'{self.user.username} <-> {self.friend.username}'
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='requests_sent')
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='requests_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username}'
    
class Block(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='blocks')
    blocked_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blocked_user')

    def __str__(self):
        return f'{self.user.username} -> {self.blocked_user.username}'

class OnlineStatus(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='online_status')
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} is {"online" if self.is_online else "offline"}'