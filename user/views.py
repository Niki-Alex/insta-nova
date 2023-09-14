from rest_framework import generics

from user.models import User
from user.serializers import UserSerializer, UserDetailSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
