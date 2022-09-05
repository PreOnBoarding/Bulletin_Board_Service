from django.urls import path, include
from user import views
from rest_framework_simplejwt.views import TokenRefreshView

# user/
urlpatterns = [
    path("", views.UserView.as_view(), name="user_view"),
    path("login", views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path('<username>', views.UserView.as_view()),
]


