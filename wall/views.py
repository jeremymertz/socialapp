from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from .models import User, Post, Comment
from notifications.models import Notification
from django.db.models import Count
from .forms import NewPostForm, NewPostForm2, PostCommentForm
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
import json
import re


def clean_text(text):
    cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleaned_text = re.sub(cleaner, '', text)
    return cleaned_text


@login_required
def home(request):
    follows = request.user.profile.followings.all()
    posts = Post.objects.filter(user__in=follows)

    context = {
        'posts': posts,
    }
    return render(request, 'wall/index.html', context)

@login_required
def most_popular(request):
    posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')

    context = {
        'posts': posts,
    }
    return render(request, 'wall/mostpopular.html', context)

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    user_followers = user.profile.followers
    user_follows = user.profile.followings
    posts = Post.objects.filter(user=user).order_by('-date_posted')

    # DM
    user_connecting = request.user
    user_to_connect_to = user
    ids = [user_connecting.id, user_to_connect_to.id]
    ids.sort()
    str_ids = 'y'.join(str(i) for i in ids)

    if request.method == "POST":

        if request.user in user_followers.all():
            user_followers.remove(request.user)
        else:
            user_followers.add(request.user)

        if user in request.user.profile.followings.all():
            request.user.profile.followings.remove(user)
        else:
            request.user.profile.followings.add(user)

    context = {
        'user': user,
        'posts': posts,
        'follows': user_follows,
        'followers': user_followers,
        'dm': str_ids
    }

    return render(request, 'wall/profile.html', context)

@login_required
def new_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.content = ''
            form.instance.date_posted = timezone.now()
            form.instance.user = request.user
            created_post = form.save()

            next_new_post_link = reverse('Next_New_Post', kwargs={'post_id': created_post.id})
            print(next_new_post_link)
            return JsonResponse({'next_new_post_link': next_new_post_link})
    else:
        form = NewPostForm()

    context = {
        'form': form,
    }
    return render(request, 'wall/new_post.html', context)

@login_required
def next_new_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        if request.method == 'POST':
            form = NewPostForm2(request.POST, instance=post)
            if form.is_valid():
                post.content = form.cleaned_data['content']
                post.hidden = False
                post.save()
                return HttpResponseRedirect(reverse('Profile', kwargs={'username': request.user.username}))
        else:
            form = NewPostForm2(instance=post)
    else:
        return redirect('home')

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'wall/next_new_post.html', context)

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        if request.method == 'POST':
            form = NewPostForm2(request.POST, instance=post)
            if form.is_valid():
                post.content = form.cleaned_data['content']
                post.hidden = False
                post.save()
                return HttpResponseRedirect(reverse('Profile', kwargs={'username': request.user.username}))
        else:
            form = NewPostForm2(instance=post)
    else:
        return redirect('home')

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'wall/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user == post.user:
        post.delete()
    else:
        return redirect('home')

    return HttpResponseRedirect(reverse('Profile', kwargs={'username': request.user.username}))

@login_required
def single_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post_id, parent=None).order_by('-ratio')
    replies = Comment.objects.filter(post=post_id).exclude(parent=None)
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            form.instance.date_posted = timezone.now()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
    else:
        form = PostCommentForm()

    context = {
        'post': post,
        'comments': comments,
        'replies': replies,
        'form': form,
    }
    return render(request, 'wall/single_post.html', context)

@login_required
def like_post(request, like):
    post = Post.objects.get(pk=like)
    post_user = post.user.username
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        notification = Notification.objects.get(
            post=post,
            user_receiving=post.user,
            user_sending=request.user,
            category="like",
        )
        notification.delete()
        liked = False
    else:
        post.likes.add(request.user)
        notification = Notification.objects.create(
            post=post,
            user_receiving=post.user,
            user_sending=request.user,
            category="like",
            message='liked your post.')
        liked = True

    context = {
        'liked': liked,
        'author': post_user,
        'user': request.user.username
    }

    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def new_comment(request, post_id):
    if request.method == 'POST':
        form = request.POST
        post = Post.objects.get(id=post_id)
        author = post.user.username
        post_number = post.id
        comment_text = clean_text(form['new_comment'])
        if len(comment_text) > 20:
            short_comment = comment_text[0:20] + '...'
        else:
            short_comment = comment_text
        empty_comment = comment_text.isspace()
        if comment_text != "" and empty_comment is False:
            now = timezone.now()
            created_comment = Comment.objects.create(post=post, user=request.user, content=comment_text, date_posted=now)
            if post.user.username != request.user.username:
                notification = Notification.objects.create(
                    post=post,
                    comment=created_comment,
                    user_sending=request.user,
                    user_receiving=post.user,
                    category="comment",
                    message=f'commented: {short_comment}',
                )
            success = True
            reply_url = HttpResponseRedirect(reverse('Reply', kwargs={'post_id': post_id}))
            like_url = HttpResponseRedirect(reverse('Like_Comment', kwargs={'comment_id': created_comment.id}))
            unlike_url = HttpResponseRedirect(reverse('Unlike_Comment', kwargs={'comment_id': created_comment.id}))
            delete_url = HttpResponseRedirect(reverse('Delete_comment', kwargs={'comment_id': created_comment.id}))
            context = {
                'success': success,
                'author': author,
                'post_number': post_number,
                'id': created_comment.id,
                'reply_url': reply_url.url,
                'like_url': like_url.url,
                'unlike_url': unlike_url.url,
                'delete_url': delete_url.url,
                'user': request.user.username
            }
        else:
            success = False
            context = {
                'success': success,
            }
        return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def reply_comment(request, post_id):
    if request.method == 'POST':
        form = request.POST
        post = Post.objects.get(id=post_id)
        reply = clean_text(form['new_reply'])
        if len(reply) > 20:
            short_comment = reply[0:20] + '...'
        else:
            short_comment = reply
        empty = reply.isspace()
        if reply != "" and empty is False:
            parent = Comment.objects.get(id=form['parent'])
            now = timezone.now()
            new_reply = Comment.objects.create(post=post, user=request.user, content=reply, date_posted=now, parent=parent)
            if post.user.username != request.user.username:
                notification = Notification.objects.create(
                    post=post,
                    comment=new_reply,
                    user_sending=request.user,
                    user_receiving=post.user,
                    category="comment",
                    message=f'commented: {short_comment}',
                )
            success = True
            like_url = HttpResponseRedirect(reverse('Like_Comment', kwargs={'comment_id': new_reply.id}))
            unlike_url = HttpResponseRedirect(reverse('Unlike_Comment', kwargs={'comment_id': new_reply.id}))
            delete_url = HttpResponseRedirect(reverse('Delete_reply', kwargs={'reply_id': new_reply.id}))
        else:
            success = False

        context = {
            'success': success,
            'new_reply_id': new_reply.id,
            'like_url': like_url.url,
            'unlike_url': unlike_url.url,
            'delete_url': delete_url.url,
            'author': post.user.username,
            'user': request.user.username,
            'post_number': post_id,
            'id': new_reply.id,
        }
        return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def like_comment(request, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(pk=comment_id)
        if request.user in comment.like.all():
            comment.like.remove(request.user)
            count = (comment.like.count()) - (comment.unlike.count())
            comment.ratio = count
            comment.save()
            liked = False
        else:
            comment.like.add(request.user)
            if request.user in comment.unlike.all():
                comment.unlike.remove(request.user)
            count = (comment.like.count()) - (comment.unlike.count())
            comment.ratio = count
            comment.save()
            liked = True

    context = {
        'liked': liked,
        'count': count,
    }

    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def unlike_comment(request, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(pk=comment_id)
        if request.user in comment.unlike.all():
            comment.unlike.remove(request.user)
            count = (comment.like.count()) - (comment.unlike.count())
            comment.ratio = count
            comment.save()
            liked = False
        else:
            comment.unlike.add(request.user)
            if request.user in comment.like.all():
                comment.like.remove(request.user)
            count = (comment.like.count()) - (comment.unlike.count())
            comment.ratio = count
            comment.save()
            liked = True

    context = {
        'liked': liked,
        'count': count,
    }

    return HttpResponse(json.dumps(context), content_type='application/json')


@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    post_id = comment.post.id
    if comment.user == request.user:
        comment.delete()
        messages.success(request, f'Your comment has been deleted!')
    else:
        messages.error(request, f'Error. Please try again later.')

    return HttpResponseRedirect(reverse('Single_Post', kwargs={'post_id': post_id}))


@login_required
def delete_reply(request, reply_id):
    reply = Comment.objects.get(pk=reply_id)
    post_id = reply.post.id
    if reply.user == request.user:
        reply.delete()
        messages.success(request, f'Your comment has been deleted!')
    else:
        messages.error(request, f'Error. Please try again later.')

    return HttpResponseRedirect(reverse('Single_Post', kwargs={'post_id': post_id}))