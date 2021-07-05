from django.shortcuts import render, HttpResponse
import json
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def notification_read(request):
    user_notifications = Notification.objects.filter(user_receiving=request.user, read=False)
    if user_notifications:
        for notification in user_notifications:
            notification.read = True
            notification.save()
            success = True
    else:
        success = False
    context = {
        'success': success
    }
    return HttpResponse(json.dumps(context), content_type='application/json')