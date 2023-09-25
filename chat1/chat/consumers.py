# # chat/consumers.py
# import json

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))
# import json

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

from .models import Message,Chat
from .serializer import ChatSerializer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .serializer import MessageSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication 

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def get_token(self, scope):
        query_string = scope.get('query_string', b'').decode('utf-8')
        params = [param.split('=') for param in query_string.split('&') if param.startswith('token=')]
        if params:
            return params[0][1]
        return None

    def fetch_messages(self, data):
        messages=Message.last_10_messages()
        messages=MessageSerializer(messages,many=True)
        messages_data = [item for item in messages.data]
        
        messages_data= messages_data[::-1]
        return self.send_chat_message(messages_data)

    def new_message(self, data):
        author=data['from']
        print(author,'authorrrr')
        content=data['message']
        print(content,'----------')
        content = {
            'command': 'new_message',
            'message': content
        }
        author='arsh2'
        author_user=User.objects.filter(username=author).first()
        group_id=self.room_group_name.split('_')[-1]
        
        chat=Chat.objects.filter(id=group_id).first()
        chat_serializer=ChatSerializer(chat)
        print(chat_serializer.data)

        message=Message.objects.create(author=author_user,content=data['message'])
        
        chat.messages.add(message)
        serializer = MessageSerializer(message)
                
        return self.send_chat_message([serializer.data])
        
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }
    
    def authenticate_token(self, token):
        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(token)
            user = auth.get_user(validated_token)
            return user
        except Exception as e:
            return None

    def connect(self):
        token = self.get_token(self.scope)
        user=self.authenticate_token(token)
        
        if user:
            self.send(text_data=json.dumps({'status': 'connected'}))
        else:
            self.send_error_message('token not valid')

            
        # self.user=user
        
         

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        

        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name, {"type": "chat.message", "message": message}
        # )
        print(data['command'],'--------------')
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        print(self.room_group_name)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
    def send_error_message(self, error_message):
        self.send(text_data=json.dumps({
            'error_message':error_message
        }))