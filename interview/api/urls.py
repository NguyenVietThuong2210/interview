from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import TopicViewSet, QuestionViewSet, UserRegistrationView, UserProfileView, VersionAPIView

router = DefaultRouter()
router.register(r"topics", TopicViewSet)
router.register(r"questions", QuestionViewSet)

urlpatterns = [
    # JWT Authentication endpoints
    path("auth/register/", UserRegistrationView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/profile/", UserProfileView.as_view(), name="user_profile"),
    path("version/", VersionAPIView.as_view(), name="api-version"),
    # Router URLs
    path("", include(router.urls)),
]
