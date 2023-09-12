from rest_framework import routers

from social_application.views import (
    CommentViewSet,
    PostViewSet,
    ReactionViewSet,
)


router = routers.DefaultRouter()
router.register("comments", CommentViewSet)
router.register("posts", PostViewSet)
router.register("reactions", ReactionViewSet)

urlpatterns = router.urls

app_name = "social_application"
