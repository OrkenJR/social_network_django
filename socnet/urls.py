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
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('<pk>/edit_profile/', ProfileEditView.as_view(), name='edit_profile'),
    path('messages/', messages, name='messages'),
    path('friends/', friends, name='friends'),
    path('groups/', groups, name='groups'),
    # path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html', form_class=LoginForm), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    url('like', like, name='like'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
