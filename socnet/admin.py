from django.contrib import admin

from socnet.models import *

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comments)
admin.site.register(Group)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(Message)
admin.site.register(Chat)

# Register your models here.
