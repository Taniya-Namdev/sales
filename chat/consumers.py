import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Chat

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Find or create the room
        self.chatroom = await self.get_or_create_room(self.room_name)
        await self.add_participant(self.chatroom, self.scope['user'])

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_or_create_room(self, room_name): 
        room, created = ChatRoom.objects.get_or_create(name=room_name) 
        if created: 
            room.creator = self.scope['user']
            room.save() 
        return room
    
    @database_sync_to_async
    def add_participant(self, chatroom, user):
        if self.scope['user'] == chatroom.creator or chatroom.participants.filter(id=user.id).exists():
            chatroom.participants.add(user)

    @database_sync_to_async 
    def remove_participant(self, chatroom, user): 
        if self.scope['user'] == chatroom.creator: 
            chatroom.participants.remove(user)

    @database_sync_to_async
    def save_message(self, room, sender, receiver, message):
        Chat.objects.create(
            room=room,
            sender=sender,
            receiver=receiver,
            content=message
        )

    @database_sync_to_async
    def get_participants(self, chatroom):
        return list(chatroom.participants.all())

    @database_sync_to_async
    def get_user_by_first_name(self, first_name):
        try:
            return User.objects.get(first_name=first_name)
        except User.DoesNotExist:
            return None

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'add_participant':
            first_name = text_data_json['first_name']
            user = await self.get_user_by_first_name(first_name)
            if user:
                await self.add_participant(self.chatroom, user)
        elif message_type == 'remove_participant':
            first_name = text_data_json['first_name']
            user = await self.get_user_by_first_name(first_name)
            if user:
                await self.remove_participant(self.chatroom, user)
        else:
            message = text_data_json['message']
            first_name = self.scope['user'].first_name
            user_id = self.scope['user'].id
            timestamp = text_data_json.get('timestamp', '')

            # Get the participants in the chatroom
            participants = await self.get_participants(self.chatroom)

            # Check if there are participants in the chatroom
            if not participants:
                await self.send(text_data=json.dumps({
                    'error': 'No participants in the chat room.'
                }))
                return

            # Send message to all participants except the sender
            for participant in participants:
                receiver = participant
                await self.save_message(self.chatroom, self.scope['user'], receiver, message)
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        'type': 'chat_message',
                        'message': message,
                        'first_name': first_name,
                        'user_id': user_id,
                        'timestamp': timestamp
                    }
                )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        first_name = event['first_name']
        user_id = event['user_id']
        timestamp = event.get('timestamp', '')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': f'{first_name}: {message} ............ {timestamp}',
            'user_id': user_id
        }))
