import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


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

    class Meta:
        ordering = ["created_at"]


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    image = models.ImageField(null=True, blank=True, upload_to=post_image_file_path)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(to=Comment, blank=True, related_name="posts")

    def __str__(self):
        return f"{self.title}, author: {self.author}"

    class Meta:
        ordering = ["created_at"]


class Reaction(models.Model):
    class ReactionTypeChoices(models.TextChoices):
        LIKE = "like"
        DISLIKE = "dislike"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    reaction_type = models.CharField(max_length=7, choices=ReactionTypeChoices.choices)

    def __str__(self):
        return f"{self.post}, {self.reaction_type}"

    class Meta:
        unique_together = ("user", "post")


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("You can't follow yourself")

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        return super(Follow, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.follower}, {self.following}"

    class Meta:
        unique_together = ("follower", "following")


class Profile(models.Model):
    nickname = models.CharField(max_length=68, unique=True)
    first_name = models.CharField(max_length=68, null=True)
    last_name = models.CharField(max_length=68, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to=profile_image_file_path)
    biography = models.TextField()
    phone_number = PhoneNumberField(null=True, blank=True)
    posts = models.ManyToManyField(to=Post, blank=True, related_name="profiles")
    followers = models.ManyToManyField(to=Follow, blank=True, related_name="following_profiles")
    followings = models.ManyToManyField(to=Follow, blank=True, related_name="follower_profiles")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ["nickname"]
