from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Message(models.Model):
    author = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def last_10_messages():
        return Message.objects.order_by('-timestamp')[:10]
        


class Chat(models.Model):
    participants = models.ManyToManyField(
        User, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)
    def get_messages(self):
        return self.messages.order_by('-timestamp')
        