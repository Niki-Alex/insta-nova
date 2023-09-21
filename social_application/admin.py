from django.contrib import admin

from social_application.models import (
    Reaction,
    Comment,
    Post,
)


admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(Post)
