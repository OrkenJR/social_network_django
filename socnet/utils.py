from django.contrib.auth.models import User

from socnet.models import FriendRequest


def get_friend_request_or_false(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False


def get_context_data(**kwargs):
    context = kwargs


def get_friend_requests(request):
    try:
        return FriendRequest.objects.filter(receiver=request.user, is_active=True)
    except FriendRequest.DoesNotExist:
        raise 0