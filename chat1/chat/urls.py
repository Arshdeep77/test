from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
     path("get/messages/<int:id>", views.fetch_message, name="room"),
     path("<str:room_name>/", views.room, name="room"),
     
     
]