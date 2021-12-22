from django import template
from django.db.models import Q

from socnet.models import FriendRequest, UserProfile, Group, Chat, Message

register = template.Library()


@register.filter
def have_parents(things):
    return things.filter(parent__isnull=True)


@register.filter
def get_image_post(post):
    if post.author is None:
        return post.group_author.image.url
    else:
        return UserProfile.objects.get(user=post.author).image.url


@register.filter
def get_post_author_url(post):
    if post.author is None:
        return "groups/" + str(post.group_author.id)
    else:
        return "profile/" + str(post.author.id)


@register.filter
def get_post_author(post):
    if post.author is None:
        return post.group_author.name
    else:
        return post.author.username


@register.filter
def friend_requests(user):
    try:
        return FriendRequest.objects.filter(receiver=user, is_active=True).count()
    except FriendRequest.DoesNotExist:
        return 0


@register.filter
def get_edit_profile_page(user):
    try:
        return "/" + str(UserProfile.objects.get(user=user).id) + "/edit_profile"
    except UserProfile.DoesNotExist:
        return "#"

@register.filter
def get_last_message(chat):
    try:
        return Message.objects.filter(chat=chat).last().text
    except Exception:
        return ""


@register.simple_tag
def get_chat_by_user(user, friend):
    try:
        return Chat.objects.filter(participants__in=[user.id, friend.id]).all()[0].id
    except Chat.DoesNotExist:
        return "#"


@register.simple_tag
def get_chat_member_name(participants, user):
    try:
        return participants.filter(~Q(pk=user.id))[0].username
    except:
        return "error"

@register.simple_tag
def get_chat_id(chat_id, user):
    if isinstance(chat_id, int):
        try:
            return Chat.objects.get(pk=chat_id).id
        except Exception as e:
            return None
        # "new/" + str(user.id)

    else:
        return None


