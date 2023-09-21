from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User, UserFollowing
from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserFollowingSerializer,
    UserFollowersSerializer,
)


class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get("username")
        first_name = self.request.query_params.get("first_name")
        date_of_birth = self.request.query_params.get("date_of_birth")

        if username:
            queryset = queryset.filter(username__icontains=username)

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if date_of_birth:
            queryset = queryset.filter(date_of_birth=date_of_birth)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=OpenApiTypes.STR,
                description="Filter by username",
            ),
            OpenApiParameter(
                "first_name",
                type=OpenApiTypes.STR,
                description="Filter by first_name",
            ),
            OpenApiParameter(
                "date_of_birth",
                type=OpenApiTypes.DATE,
                description="Filter by date_of_birth",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)


class UserFollowingView(generics.ListAPIView):
    serializer_class = UserFollowingSerializer
    pagination_class = Pagination

    def get_queryset(self):
        current_user = self.request.user
        queryset = UserFollowing.objects.filter(user_id=current_user)

        return queryset


class UserFollowersView(generics.ListAPIView):
    serializer_class = UserFollowersSerializer
    pagination_class = Pagination

    def get_queryset(self):
        current_user = self.request.user
        queryset = UserFollowing.objects.filter(following_user_id=current_user)

        return queryset


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class LogoutTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.data.get("token")

        if token:
            refresh_token = RefreshToken(token)
            refresh_token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

        return Response({"error": "Failed to logout"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserAddFollow(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User is not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def post(self, request, pk):
        user = request.user
        follow = self.get_object(pk)
        if user == follow:
            raise ValidationError("You can't follow to yourself")
        UserFollowing.objects.create(user_id=user, following_user_id=follow)
        serializer = UserDetailSerializer(follow)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = request.user
        follow = self.get_object(pk)
        action = UserFollowing.objects.filter(user_id=user, following_user_id=follow)
        action.delete()
        serializer = UserDetailSerializer(follow)
        return Response(serializer.data)
