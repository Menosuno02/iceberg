from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

from friend.models import FriendList

from .models import Chat, Room

""" Lista de chats """
@login_required
def room_enroll(request):
    friends = FriendList.objects.filter(user=request.user)[0].friends.all()
    all_rooms = Room.objects.filter(Q(author=request.user) | Q(friend=request.user)).order_by('-created')
    context = {
        'all_rooms':all_rooms,
        'all_friends':friends,
    }
    return render(request, 'chat/join_room.html', context)


""" Función para validar si existe sala """
@login_required
def room_choice(request, friend_id):
    friend = User.objects.filter(pk=friend_id)
    if not friend:
        messages.error(request, 'ID inválida')
        return redirect('room-enroll') 
    if not FriendList.objects.filter(user=request.user, friends=friend[0]):
        messages.error(request, 'Necesitais ser amigos para chatear')
        return redirect('room-enroll') 
    room = Room.objects.filter(Q(author=request.user, friend=friend[0]) | Q(author=friend[0], friend=request.user))
    if not room:
        create_room = Room(author=request.user, friend=friend[0])
        create_room.save()
        room = create_room.room_id
        return redirect('room', room, friend_id)
    return redirect('room', room[0].room_id, friend_id)


""" Chat """
@login_required
def room(request, room_name, friend_id):
    all_rooms = Room.objects.filter(room_id=room_name)
    if not all_rooms:  
        messages.error(request, 'ID de chat inválida')
        return redirect('room-enroll')
    chats = Chat.objects.filter(room_id=room_name).order_by('date')
    context = {
        'old_chats':chats,
        'my_name':request.user,
        'friend_name':User.objects.get(pk=friend_id),
        'room_name': room_name
    }
    return render(request, 'chat/chatroom.html', context)