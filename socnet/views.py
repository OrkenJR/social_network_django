from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Post, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django import template

register = template.Library()



def like(request):

    post = Post.objects.get(id=request.POST.get("post_id"))
    type = request.POST.get('type')
    current_user = request.user
    is_liked = False
    # post.likes.get(id=current_user.id)

    if type == 'like':
        for like in post.likes.all():
            if like == current_user:
                is_liked = True
                break

        if not is_liked:
            post.dislikes.remove(current_user)
            post.likes.add(current_user)

    else:
        for dislike in post.dislikes.all():
            if dislike == current_user:
                is_liked = True
                break
        if not is_liked:
            post.dislikes.add(current_user)
            post.likes.remove(current_user)



    context = {
        "posts": Post.objects.all()
    }
    return render(request, "posts/posts.html", context)


@login_required
def home(request):
    current_user = request.user
    context = {
        "posts": Post.objects.all()
    }
    return render(request, "posts/posts.html", context)


def profile(request):
    current_user = request.user
    context = {
        "posts": Post.objects.all(),
        "user": current_user,
        "profile": UserProfile.objects.get(user_id=current_user.id)
    }
    return render(request, 'profile/profile.html', context)


def messages(request):
    return render(request, 'messages-list/messages-list.html')


def friends(request):
    return render(request, 'friends-list/friends-list.html')


def groups(request):
    return render(request, 'groups-list/groups-list.html')


@login_required
def logout(request):
    django_logout(request)
    return redirect('/login')


def login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            return redirect('/')
        else:
            return redirect('/login')

    return render(request, 'login/login.html')
