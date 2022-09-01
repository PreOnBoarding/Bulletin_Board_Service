from django.urls import path, include
from .views import UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# user/
urlpatterns = [
    path("", UserView.as_view()),
    path('<username>/', UserView.as_view()),
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
