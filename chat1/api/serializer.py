from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        fields=['id','username','email']
    
    def validate_password(self, password):
        if not password or not isinstance(password, str) or not len(password):
            raise serializers.ValidationError("Invalid Password.")
        elif len(password) < 8 :
            raise serializers.ValidationError("Password must be atleast 8 characters")
        return password
