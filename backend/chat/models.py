from django.db import models
from users.models import Account

class RoomName(models.Model):
    Conversation_Choices = [
        ('group', 'group'),
        ('private', 'private')
    ]

    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Account, related_name='rooms')
    conversation_type = models.CharField(max_length=10, choices=Conversation_Choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_members(self):
        return self.members.all()
    
    def get_messages(self):
        return RoomMessages.objects.filter(room=self)
    

class RoomMessages(models.Model):
    room = models.ForeignKey(RoomName, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.TextField()
    # unread = models.BooleanField(default=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    