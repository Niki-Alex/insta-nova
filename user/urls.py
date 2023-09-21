from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from user.views import (
    CreateUserView,
    UserDetailView,
    UserListView,
    UserUpdateView,
    UserAddFollow,
    UserFollowingView,
    UserFollowersView,
    LogoutTokenView,
)


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user-create"),
    path("update/", UserUpdateView.as_view(), name="user-update"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("", UserListView.as_view(), name="users-all"),
    path("following/", UserFollowingView.as_view(), name="user-following"),
    path("followers/", UserFollowersView.as_view(), name="user-followers"),
    path("follow/<int:pk>/", UserAddFollow.as_view(), name="user-add-follow"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutTokenView.as_view(), name="logout"),
]

app_name = "user"
