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
import socnet.views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', socnet.views.home, name='home'),
    path('profile/', socnet.views.profile, name='profile'),
    path('messages/', socnet.views.messages, name='messages'),
    path('friends/', socnet.views.friends, name='friends'),
    path('groups/', socnet.views.groups, name='groups'),
    # path('login/', socnet.views.login, name='login'),
    path('logout/', socnet.views.logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    url('like', socnet.views.like, name='like'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
