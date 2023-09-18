from rest_framework import routers

from social_application.views import (
    CommentViewSet,
    PostViewSet,
    UserPostsViewSet,
    ReactionViewSet,
)


router = routers.DefaultRouter()
router.register("comments", CommentViewSet)
router.register("posts", PostViewSet, basename="post")
router.register("user_posts", UserPostsViewSet, basename="user_posts")
router.register("reactions", ReactionViewSet)

urlpatterns = router.urls

app_name = "social_application"
