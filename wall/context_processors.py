from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from sockets.models import Channel
from django.db.models import Q

def add_variable_to_context(request):
    if request.user.is_authenticated:
        user_active_channels = Channel.objects.filter(Q(User1=request.user) | Q(User2=request.user))
        new_message = False
        for channel in user_active_channels:
            if channel.read is False and channel.last_message_author != request.user:
                new_message = True

        return {
            'notifications': Notification.objects.all().filter(user_receiving=request.user).order_by('-timestamp'),
            'user_active_channels': user_active_channels,
            'new_message': new_message
        }
    else:
        return {}
