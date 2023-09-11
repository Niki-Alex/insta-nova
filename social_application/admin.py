from django.contrib import admin

from social_application.models import (
    Reaction,
    Comment,
    Post,
    Follow,
    Profile
)


admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Profile)
