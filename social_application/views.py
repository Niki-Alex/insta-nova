from django.db.models import Q
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

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


class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("post", "author")
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CommentListSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all().select_related("author", "post")
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
    pagination_class = Pagination
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
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = Pagination
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
