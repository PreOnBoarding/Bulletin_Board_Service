from django.urls import path, include
from .views import UserView

# user/
urlpatterns = [
    path('<username>/', UserView.as_view())
]
