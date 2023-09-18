from django.contrib import admin

from user.models import User, UserFollowing

admin.site.register(User)
admin.site.register(UserFollowing)
