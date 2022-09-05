from django.urls import path
from statistic import views

# statistic/
urlpatterns = [
    path('gender', views.GenderStatisticsView.as_view()),
]