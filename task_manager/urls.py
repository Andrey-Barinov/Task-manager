from django.contrib import admin
from django.urls import path, include
from task_manager import views

app_name = 'task_manager'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]
