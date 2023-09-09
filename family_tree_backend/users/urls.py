"""Defines URL patterns for users"""
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name='users'

urlpatterns = [
        #Admin login page
        path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
        #Admin logout page
        path('logout/', views.admin_logout, name='logout'),
        ]
