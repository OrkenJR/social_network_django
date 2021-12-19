from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from .forms import *
from .models import Post, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
import json

from .utils import get_friend_request_or_false


class FriendListView(ListView):
    model = UserProfile
    template_name = 'friends-list/friends-list.html'
    context_object_name = 'friends'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        context['query_set'] = serializers.serialize('json',
                                                     FriendList.objects.get(user=self.request.user).friends.all())
        context['profile_query_set'] = serializers.serialize('json', UserProfile.objects.filter(
            user__in=FriendList.objects.get(user=self.request.user).friends.all()).all())
        return context

    def get_queryset(self):
        return UserProfile.objects.filter(user__in=FriendList.objects.get(user=self.request.user).friends.all()).all()


def delete_friend(request):
    user = request.user
    response = {}
    if request.method == "POST":
        user_id = request.POST.get("receiver_id")
        if user_id:
            try:
                friend = User.objects.get(pk=user_id)
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfriend(friend)
                response['response'] = "success"
            except Exception as e:
                response['response'] = "error"
        else:
            response['response'] = "error"

    return JsonResponse(response)


def accept_friend_request(request):
    user = request.user
    response = {}
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        if request_id:
            friend_request = FriendRequest.objects.get(pk=request_id)
            if friend_request:
                if friend_request.receiver == user:
                    friend_request.accept()
                    response['response'] = "success"
                else:
                    response['response'] = 'error'
        else:
            response['response'] = 'error'

    return JsonResponse(response)


def cancel_friend_request(request):
    user = request.user
    response = {}
    if request.method == "POST":
        receiver_id = request.POST.get("receiver_id")
        if receiver_id:
            receiver = User.objects.get(pk=receiver_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                try:
                    for friend_request in friend_requests:
                        if friend_request.is_active:
                            friend_request.delete()
                            response['response'] = "success"
                            break
                        else:
                            response['response'] = "error"
                except Exception as e:
                    response['response'] = str(e)
            except FriendRequest.DoesNotExist:
                response['response'] = "error"

            if response['response'] is None:
                response['response'] = 'error'
    else:
        response['response'] = 'error'
    return JsonResponse(response)


def send_friend_request(request):
    user = request.user
    response = {}
    if request.method == 'POST':
        receiver_id = request.POST.get("receiver_id")
        if receiver_id:
            receiver = User.objects.get(pk=receiver_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                try:
                    for friend_request in friend_requests:
                        if friend_request.is_active:
                            raise Exception("Вы уже оставили заявку на дружбу")
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    response['response'] = "success"
                except Exception as e:
                    response['response'] = str(e)
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                response['response'] = "success"

            if response['response'] == None:
                response['response'] = 'error'



        else:
            response['response'] = 'error'

    return JsonResponse(response)


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
            if parent_id and parent_id != 0:
                parent_obj = Comments.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
                    replay_comment.user = current_user
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = current_user
            new_comment.save()

            response = {
                'comment_id': new_comment.id,
                'post_id': new_comment.post.id,
                'comment_body': new_comment.body,
                'author': new_comment.user.username,
                'parent_id': parent_id,
                'date': new_comment.calculate_days_ago()
            }

            return JsonResponse(response)
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


def ProfileView(request):
    return redirect('/profile/' + str(request.user.id))
    # model = Post
    # template_name = 'profile/profile.html'
    # context_object_name = 'posts'
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['user'] = self.request.user
    #     context['profile'] = UserProfile.objects.get(user_id=self.request.user.id)
    #     try:
    #         friend_list = FriendList.objects.get(user=self.request.user)
    #     except FriendList.DoesNotExist:
    #         friend_list = FriendList(user=self.request.user)
    #         friend_list.save()
    #     my_friends = friend_list.friends.all()
    #     context['friends'] = my_friends
    #
    #     return context
    #
    # def get_queryset(self):
    #     return Post.objects.order_by('-date_posted')


class ProfileViewOther(DetailView):
    model = User
    template_name = 'profile/profile.html'

    def get_user_profile(self, username):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ProfileViewOther, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['this_user'] = User.objects.get(pk=self.kwargs.get('pk'))
        context['profile'] = UserProfile.objects.get(user=context['this_user'])
        context['my_profile'] = UserProfile.objects.get(user=self.request.user)
        context['posts'] = Post.objects.filter(author=User.objects.get(pk=self.kwargs.get('pk')))

        try:
            friend_list = FriendList.objects.get(user=self.request.user)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=self.request.user)
            friend_list.save()

        my_friends = friend_list.friends.all()
        context['my_friends'] = my_friends

        try:
            friend_list = FriendList.objects.get(user=context['this_user'])
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=context['this_user'])
            friend_list.save()
        context['friends'] = friend_list.friends.all()

        is_my_account = True
        is_friend_account = False
        user = self.request.user
        friend_request = "0"
        friend_requests = None
        if user.id != self.kwargs.get("pk"):
            is_my_account = False
            if my_friends.filter(pk=self.kwargs.get('pk')):
                is_friend_account = True
            else:
                is_friend_account = False

                if get_friend_request_or_false(sender=context.get("this_user"), receiver=user):
                    friend_request = "from"
                    context["friend_request"] = get_friend_request_or_false(sender=context.get("this_user"),
                                                                            receiver=user).id

                elif get_friend_request_or_false(sender=user, receiver=context.get("this_user")):
                    friend_request = "to"
                    context["friend_request"] = get_friend_request_or_false(sender=user,
                                                                            receiver=context.get("this_user")).id
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=context.get("this_user"), is_active=True)
            except Exception as e:
                raise e

        context["is_me"] = is_my_account
        context["is_friend"] = is_friend_account
        context["friend_request_enum"] = friend_request
        context["friend_requests"] = friend_requests

        return context


class PostCreationView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['body', 'image']
    template_name = 'posts/create_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.group_author = Group.objects.get(admin=self.request.user)
        return super().form_valid(form)


class PostCreationGroup(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['body', 'image']
    template_name = 'posts/create_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.group_author = Group.objects.get(admin=self.request.user)
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


class GroupView(DetailView):
    model = Group
    template_name = 'group/group.html'

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        try:
            context['posts'] = Post.objects.filter(group_author=Group.objects.get(pk=self.kwargs.get('pk'))).all()
        except Post.DoesNotExist:
            context['posts'] = 'null'
        return context


class GroupList(ListView):
    model = Group
    template_name = 'groups-list/groups-list.html'
    context_object_name = 'groups'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        # Group.objects.filter(followers__in=self.request.user).all()
        return Group.objects.filter(
            followers__username__contains=self.request.user.username).all() | Group.objects.filter(
            admin=self.request.user).all()
        # return Group.objects.filter(admin=self.request.user).all()


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
