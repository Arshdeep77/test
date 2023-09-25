from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from chat.models import Chat
from chat.serializer import ChatSerializer
from .serializer import UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication
@api_view(['POST'])
def login(request):
    
    user=get_object_or_404(User,username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"detail":"Not found"},status=status.HTTP_400_BAD_REQUEST)
    token=RefreshToken.for_user(user)
    serializer=UserSerializer(instance=user)
    user.is_active=True
    user.save() 
    return Response({'refresh_token':str(token),'access':str(token.access_token),"user":serializer.data})

    
@api_view(['POST'])
def signup(request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user=User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.is_active=True
        user.save()
        
        token=RefreshToken.for_user(user)
        return Response({'refresh_token':str(token),'access':str(token.access_token),"user":serializer.data})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def start_chat(request,id):
    user_id_1=request.user.id
    user_id_2=int(id)
    if user_id_1==user_id_2:
        return Response({'message':'action not allowed'},status=400)

    chat_rooms = Chat.objects.filter(participants=user_id_1).filter(participants=user_id_2).first()
    
    if not chat_rooms:
        
        id1=1
        chat_room = Chat.objects.create()
        id=int(id)
        id1=int(id1)
        u2=User.objects.filter(id=id1).first()
        u1=User.objects.filter(id=id).first()
        if not  u1:
            
            return Response({'message':'user nor exist'},status=400)  
      
        chat_room.participants.add(u1)
        chat_room.participants.add(u2)
        chat_room.save()
        return Response({'message':'room created','room_id':chat_room.id},status=200)
        
    else:
        
        return Response({'message':'room present','room_id':chat_rooms.id},status=200)
        

       


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_active_users(request):
        try:
            # Get users with is_active = 1
            active_users = User.objects.filter(is_active=1)
            serializer = UserSerializer(active_users, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'An error occurred'},status=status.HTTP_400_BAD_REQUEST)
    