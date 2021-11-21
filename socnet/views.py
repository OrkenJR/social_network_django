from django.http import HttpResponse
from django.shortcuts import render
from .models import Post


def home(request):
    context ={
        "posts": Post.objects.all()
    }
    return render(request, "posts/posts.html", context)


def profile(request):
    return render(request, 'profile/profile.html')


def messages(request):
    return render(request, 'messages-list/messages-list.html')


def friends(request):
    return render(request, 'friends-list/friends-list.html')


def groups(request):
    return render(request, 'groups-list/groups-list.html')
