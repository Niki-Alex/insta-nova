from django.urls import path

from user.views import (
    CreateUserView,
    UserDetailView,
    UserListView,
    UserUpdateView,
    UserAddFollow,
    UserFollowingView,
    UserFollowersView,
)


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user-create"),
    path("update/", UserUpdateView.as_view(), name="user-update"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("", UserListView.as_view(), name="users-all"),
    path("following/", UserFollowingView.as_view(), name="user-following"),
    path("followers/", UserFollowersView.as_view(), name="user-followers"),
    path("follow/<int:pk>/", UserAddFollow.as_view(), name="user-add-follow"),
]

app_name = "user"
