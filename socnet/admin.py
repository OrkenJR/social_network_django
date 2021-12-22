from django.contrib import admin

from socnet.models import Post, UserProfile, Comments, Group

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comments)
admin.site.register(Group)
# Register your models here.
