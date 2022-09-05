from django.urls import path

from . import views

urlpatterns = [
    path("<int:post_type>", views.PostView.as_view()),
    path("edit/<int:post_id>", views.PostView.as_view()),
]
