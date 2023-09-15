from django.db.models import Q, F, Count, Case, When, IntegerField
from rest_framework import viewsets

from social_application.models import (
    Comment,
    Post,
    Reaction,
)

from social_application.serializers import (
    ReactionSerializer,
    CommentSerializer,
    CommentListSerializer,
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
    ReactionListSerializer,
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CommentListSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReactionListSerializer
        return ReactionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # def get_queryset(self):
    #     queryset = self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
