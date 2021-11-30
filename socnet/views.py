from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .forms import *
from .models import Post, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout


def post_comment(request):


    post = Post.objects.get(id=request.POST.get("post_id"))

    current_user = request.user
    comments = post.comments.filter(parent__isnull=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id and parent_id!=0:
                parent_obj = Comments.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
                    replay_comment.user = current_user
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = current_user
            new_comment.save()



            # data = serializers.serialize('json',  post.comments.all())
            response = {
                'comment_id': new_comment.id,
                'post_id': new_comment.post.id,
                'comment_body': new_comment.body,
                'author': new_comment.user.username,
                'parent_id': parent_id,
                'date':new_comment.calculate_days_ago()
            }
            return JsonResponse(response)
            # return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    return render(request,
                  'posts/posts.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})


def like(request):
    post = Post.objects.get(id=request.POST.get("post_id"))
    type = request.POST.get('type')
    current_user = request.user
    is_liked = False
    if type == 'like':
        for like in post.likes.all():
            if like == current_user:
                is_liked = True
                break

        if not is_liked:
            post.dislikes.remove(current_user)
            post.likes.add(current_user)
        else:
            post.likes.remove(current_user)

    else:
        for dislike in post.dislikes.all():
            if dislike == current_user:
                is_liked = True
                break
        if not is_liked:
            post.dislikes.add(current_user)
            post.likes.remove(current_user)
        else:
            post.dislikes.remove(current_user)

    response = {
        'is_liked': is_liked,
        'likes': post.likes.count() - post.dislikes.count()
    }
    return JsonResponse(response)


@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    comment_form = CommentForm()


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['c_form'] = self.comment_form
        return context

    def get_queryset(self):
        return Post.objects.order_by('-date_posted')


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'register/register.html'
    success_message = "You were successfully registered to SmallTalk. Please Sign In"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        profile = UserProfile(user=user, quote='')
        profile.save()

        return super().form_valid(form)


class ProfileEditView(UpdateView):
    model = UserProfile
    template_name = 'profile/edit_profile.html'
    fields = ['image', 'quote', 'birth_date']
    success_url = '/profile'

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        profile_form = ProfileUpdateForm(self.request.POST,
                                         self.request.FILES,
                                         instance=UserProfile.objects.get(user=self.request.user))

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = UserProfile.objects.get(user_id=self.request.user.id)
        if self.request.method == 'GET':
            user_form = UserUpdateForm(instance=self.request.user)
            profile_form = ProfileUpdateForm(instance=UserProfile.objects.get(user=self.request.user))

        context['user_form'] = user_form
        context['profile_form'] = profile_form

        return context


class ProfileView(ListView):
    model = Post
    template_name = 'profile/profile.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = UserProfile.objects.get(user_id=self.request.user.id)

        return context

    def get_queryset(self):
        return Post.objects.order_by('-date_posted')


class PostCreationView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['body', 'image']
    template_name = 'posts/create_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(UpdateView):
    model = Post
    fields = ['body', 'image']
    template_name = 'posts/edit_post.html'
    success_url = '/'


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/posts.html'
    success_url = '/'


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


def register(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            return redirect('/')
        else:
            return redirect('/login')

    return render(request, 'register/register.html')
