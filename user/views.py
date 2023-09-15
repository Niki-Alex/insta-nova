from django.http import Http404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User, UserFollowing
from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserFollowingSerializer,
    UserFollowersSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

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


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserFollowingView(generics.ListAPIView):
    serializer_class = UserFollowingSerializer

    def get_queryset(self):
        current_user = self.request.user
        queryset = UserFollowing.objects.filter(user_id=current_user)

        return queryset


class UserFollowersView(generics.ListAPIView):
    serializer_class = UserFollowersSerializer

    def get_queryset(self):
        current_user = self.request.user
        queryset = UserFollowing.objects.filter(following_user_id=current_user)

        return queryset


class UserAddFollow(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Http404

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
