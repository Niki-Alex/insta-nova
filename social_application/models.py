import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


def custom_image_file_path(instance, filename, folder):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", folder, filename)


def post_image_file_path(instance, filename):
    return custom_image_file_path(instance, filename, "posts")


def profile_image_file_path(instance, filename):
    return custom_image_file_path(instance, filename, "profiles")


class Comment(models.Model):
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}, {self.created_at}"


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    image = models.ImageField(null=True, upload_to=post_image_file_path)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(to=Comment, related_name="posts")

    def __str__(self):
        return f"{self.title}, author: {self.author}"


class Reaction(models.Model):
    class ReactionTypeChoices(models.TextChoices):
        LIKE = "like"
        DISLIKE = "dislike"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    reaction_type = models.CharField(max_length=7, choices=ReactionTypeChoices.choices)

    def __str__(self):
        return f"{self.post}, {self.reaction_type}"


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )

    def __str__(self):
        return f"{self.follower}, {self.following}"


class Profile(models.Model):
    nickname = models.CharField(max_length=68, unique=True)
    first_name = models.CharField(max_length=68, null=True)
    last_name = models.CharField(max_length=68, null=True)
    photo = models.ImageField(null=True, upload_to=profile_image_file_path)
    biography = models.TextField()
    phone_number = models.IntegerField()
    posts = models.ManyToManyField(to=Post, related_name="profiles")
    followers = models.ManyToManyField(to=Follow, related_name="following_profiles")
    followings = models.ManyToManyField(to=Follow, related_name="follower_profiles")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def clean(self):
        if self.phone_number != 10:
            raise ValidationError("Phone number must contain 10 digits")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Profile, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return self.nickname
