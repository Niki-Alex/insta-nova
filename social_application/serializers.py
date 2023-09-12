from rest_framework import serializers

from social_application.models import (
    Comment,
    Post,
    Reaction,
    Follow,
    Profile,
)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content", "author", "created_at")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "content", "image", "author", "created_at", "comments")


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("id", "user", "post", "reaction_type")


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "follower", "following")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "nickname",
            "first_name",
            "last_name",
            "photo",
            "biography",
            "phone_number",
            "posts",
            "followers",
            "followings",
            "user",
        )
