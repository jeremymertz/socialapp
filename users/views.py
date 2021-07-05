from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, redirect
from notifications.models import Notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            new_user = User.objects.get(username=username)
            admin = User.objects.get(username='Rei')
            welcome = Notification.objects.create(
                user_sending=admin,
                user_receiving=new_user,
                message=f'Welcome to Social Impact! Have fun!'
            )
            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def login(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user': user,
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/edit_profile.html', context)
