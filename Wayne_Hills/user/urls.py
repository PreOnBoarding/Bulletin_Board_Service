from django.urls import path, include
from .views import UserView

# user/
urlpatterns = [
    path("", UserView.as_view()),
    path('<username>/', UserView.as_view())
]
