from django.urls import path

from . import views

urlpatterns = [
    path("", views.GeneralPostView.as_view()),
    path("<int:general_post_id>", views.GeneralPostView.as_view()),
]