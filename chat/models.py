from django.db import models

# Create your models here.
from django.conf import settings
from softdelete.models import SoftDeleteObject

User = settings.AUTH_USER_MODEL

class Chat(SoftDeleteObject,models.Model):
    
    content = models.CharField(max_length=1000,null=False,blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE , related_name = 'sent_messages',default=0)
    receiver = models.ForeignKey(User,on_delete=models.CASCADE , related_name = 'recieved_messages',default=0)
    room = models.ForeignKey('ChatRoom',on_delete = models.CASCADE,related_name = 'messages')

    def __str__(self):
        return f'{self.sender.first_name} to {self.receiver.first_name} : {self.content[:50]}'
    
class ChatRoom(models.Model):
    name = models.CharField(max_length=200, unique = True)
    participants = models.ManyToManyField(User,related_name='chatrooms')
    creator = models.ForeignKey(User,related_name='created_rooms',on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.name