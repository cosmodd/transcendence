from django.db import models
from django.contrib.auth.models import User

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}'

class Block(models.Model):
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked')
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker')

    def __str__(self):
        return f'{self.blocker.username} blocked {self.blocked.username}'