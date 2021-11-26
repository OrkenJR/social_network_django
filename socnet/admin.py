from django.contrib import admin

from socnet.models import Post, UserProfile, Comments

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comments)
# Register your models here.
