from rest_framework import serializers
from django.contrib.auth.models import User
from . models import Chat,Message
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        fields=['id','username','password','email']
    
    def validate_password(self, password):
        if not password or not isinstance(password, str) or not len(password):
            raise serializers.ValidationError("Invalid Password.")
        elif len(password) < 8 :
            raise serializers.ValidationError("Password must be atleast 8 characters")
        return password
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model=Chat
        fields='__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'author', 'content', 'timestamp')  # Define the fields you want to include in the serialized output