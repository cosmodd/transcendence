from django.db import models
from users.models import Account

class Conversation(models.Model):
    CONVERSATION_TYPE_CHOICES = ['direct', 'group']

    type = models.CharField(max_length=10, choices=CONVERSATION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserConversation(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'conversation')


class WebsocketToken(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=36)