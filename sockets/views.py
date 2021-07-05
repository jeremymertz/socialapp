from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Channel, Message
from django.http import JsonResponse
from django.utils import timezone


def get_users_and_room(room_name, user1_id, user2_id, request_user):
    # get users
    try:
        user1 = User.objects.get(pk=user1_id)
    except ObjectDoesNotExist:
        return redirect('home')
    try:
        user2 = User.objects.get(pk=user2_id)
    except ObjectDoesNotExist:
        return redirect('home')

    if request_user == user1 or request_user == user2 and user1 != user2:
        # Create or get channel
        channel, created = Channel.objects.get_or_create(
            channel_name=room_name,
            User1=User.objects.get(pk=user1_id),
            User2=User.objects.get(pk=user2_id),
        )
    else:
        return redirect('home')

    if user1 == request_user:
        sender = user1
        receiver = user2
    else:
        sender = user2
        receiver = user1

    return user1, user2, channel, sender, receiver

@login_required
def index(request):
    return render(request, 'sockets/index.html')


@login_required
def room(request, room_name):
    user1_id, user2_id = room_name.split('y')
    if user1_id == user2_id:
        return redirect('home')
    else:
        user1, user2, channel, sender, receiver = get_users_and_room(room_name, user1_id, user2_id, request.user)

    messages = list(Message.objects.filter(channel=channel))

    if request.user != channel.last_message_author and channel.read is False:
        channel.read = True
        channel.save()

    context = {
        'room_name': room_name,
        'messages': messages,
        'channel_name': channel.channel_name,
        'sender': sender,
        'receiver': receiver,
    }

    return render(request, 'sockets/room.html', context)
