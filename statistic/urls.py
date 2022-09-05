from django.urls import path
from statistic import views

# statistic/
urlpatterns = [
    path('gender', views.GenderStatisticsView.as_view()),
    path('age', views.AgeStatisticsView.as_view()),
    path('logintime', views.LoginTimeStatisticsView.as_view()),
]