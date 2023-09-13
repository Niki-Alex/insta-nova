import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "posts", filename)


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    image = models.ImageField(null=True, upload_to=post_image_file_path)
    author = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtag = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}, author: {self.author.username}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        "user.User", on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}, {self.created_at}"

    class Meta:
        ordering = ["created_at"]


class Reaction(models.Model):
    class ReactionTypeChoices(models.TextChoices):
        LIKE = "like"
        DISLIKE = "dislike"

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    reaction_type = models.CharField(max_length=7, choices=ReactionTypeChoices.choices)

    def __str__(self):
        return f"{self.post.title} {self.reaction_type}d by {self.user}"
