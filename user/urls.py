from django.urls import path

from user.views import CreateUserView, UserDetailView


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("<int:pk>/", UserDetailView.as_view(), name="detail_user"),
]

app_name = "user"
