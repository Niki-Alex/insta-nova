from django.db.models import Q, F, Count
from rest_framework import viewsets

from social_application.models import (
    Comment,
    Post,
    Reaction,
    Follow,
    Profile,
)

from social_application.serializers import (
    CommentSerializer,
    PostSerializer,
    ReactionSerializer,
    FollowSerializer,
    ProfileSerializer,
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
