from django.db.models import Q
from rest_framework import viewsets, generics

from social_application.models import (
    Comment,
    Post,
    Reaction,
)
from social_application.permissions import IsOwnerOrReadOnly

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
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CommentListSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReactionListSerializer
        return ReactionSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related("author")
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        title = self.request.query_params.get("title")
        hashtag = self.request.query_params.get("hashtag")

        if title:
            queryset = queryset.filter(title__icontains=title)

        if hashtag:
            queryset = queryset.filter(hashtag__icontains=hashtag)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserPostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        current_user = self.request.user

        queryset = Post.objects.filter(
            Q(author=current_user)
            | Q(author__in=current_user.following.values("following_user_id"))
        )

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostListSerializer
