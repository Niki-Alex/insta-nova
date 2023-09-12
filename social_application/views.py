from django.db.models import Q, F, Count
from rest_framework import viewsets

from social_application.models import (
    Comment,
    Post,
    Reaction,
)

from social_application.serializers import (
    CommentSerializer,
    PostSerializer,
    ReactionSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
