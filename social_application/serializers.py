from rest_framework import serializers

from social_application.models import (
    Comment,
    Post,
    Reaction,
)


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("id", "post", "reaction_type")

    def validate(self, data):
        reaction = Reaction.objects.filter(
            post_id=data["post"], user_id=data["user"]
        )
        if reaction:
            raise serializers.ValidationError(
                "You had already reaction this post"
            )
        return data


class ReactionListSerializer(ReactionSerializer):
    post = serializers.ReadOnlyField(source="post.title")
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Reaction
        fields = ("id", "post", "user", "reaction_type")


class ReactionDetailSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    reaction = serializers.ReadOnlyField(source="reaction_type")

    class Meta:
        model = Reaction
        fields = ("id", "username", "reaction")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "content", "created_at")


class CommentListSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source="post.title")
    author = serializers.ReadOnlyField(source="author.username")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    comment = serializers.ReadOnlyField(source="content")

    class Meta:
        model = Comment
        fields = ("id", "post", "author", "comment", "created_at")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "content", "image", "created_at", "hashtag")


class PostListSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    @staticmethod
    def get_comments_count(obj) -> int:
        return obj.comments.count()

    @staticmethod
    def get_likes_count(obj) -> int:
        like = obj.reactions.filter(reaction_type="like")
        return like.count()

    @staticmethod
    def get_dislikes_count(obj) -> int:
        dislike = obj.reactions.filter(reaction_type="dislike")
        return dislike.count()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "image",
            "created_at",
            "hashtag",
            "comments_count",
            "likes_count",
            "dislikes_count",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    comments = CommentListSerializer(many=True, read_only=True)
    reactions = ReactionDetailSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "image",
            "author",
            "created_at",
            "hashtag",
            "comments",
            "reactions",
        )
