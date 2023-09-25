from django.shortcuts import render
from .models import Message
from .models import Chat
from .serializer import MessageSerializer
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
@api_view(["Get"])
@permission_classes([IsAuthenticated])
def fetch_message(request,id):
    
    chat=Chat.objects.filter(id=id).first()
    
    messages_data=[]
    if chat:
        messages=chat.get_messages()
        messages=MessageSerializer(messages,many=True)
        messages_data = [item for item in messages.data]
        
        messages_data= messages_data[::-1]
    return Response({"data":messages_data})
@api_view(['GET'])
def index(request):
    return render(request, "chat/index.html")
@api_view(['GET'])
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})