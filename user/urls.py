from django.urls import path

from user.views import CreateUserView, UserDetailView, UserListView, UserUpdateView


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user-create"),
    path("", UserListView.as_view(), name="users-all"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("update/", UserUpdateView.as_view(), name="users-update"),
]

app_name = "user"
