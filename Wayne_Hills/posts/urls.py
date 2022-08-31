from django.urls import path

from . import views

urlpatterns = [
    path("", views.GeneralPostView.as_view()),
]