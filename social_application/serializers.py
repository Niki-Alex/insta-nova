from rest_framework import serializers

from social_application.models import (
    Comment,
    Post,
    Reaction,
)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "content", "image", "author", "created_at", "hashtag")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "content", "author", "created_at")


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("id","user", "post", "reaction_type")
