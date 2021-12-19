"""social_network_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .forms import LoginForm
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/edit/<int:pk>', PostEditView.as_view(), name='post_edit'),
    path('post/new/', PostCreationView.as_view(), name='post_create'),
    path('post/new_group/', PostCreationGroup.as_view(), name='post_create_group'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('profile/', ProfileView, name='profile'),
    path('profile/<int:pk>', ProfileViewOther.as_view(), name='profile_view_others'),
    path('<pk>/edit_profile/', ProfileEditView.as_view(), name='edit_profile'),
    path('messages/', messages, name='messages'),
    path('friends/', FriendListView.as_view(), name='friends'),
    path('groups/', GroupList.as_view(), name='groups'),
    path('groups/<int:pk>', GroupView.as_view(), name='group'),
    path('logout/', logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html', form_class=LoginForm), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    url('like', like, name='like'),
    url('post_comment', post_comment, name='post_comment'),
    url('send_friend_request', send_friend_request, name='send_friend_request'),
    url('cancel_friend_request', cancel_friend_request, name='cancel_friend_request'),
    url('accept_friend_request', accept_friend_request, name='accept_friend_request'),
    url('delete_friend', delete_friend, name='delete_friend'),
    url('follow_group', follow_group, name='follow_group'),
    url('unfollow', unfollow, name='unfollow'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
