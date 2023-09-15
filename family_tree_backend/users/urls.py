"""Defines URL patterns for users"""
from django.urls import path
from . import views

app_name='users'

urlpatterns = [
        #Admin login page
        path('api/login/', views.login_view.as_view(), name='login'),

        path('api/logout/', views.logout_view.as_view(), name='logout'),
        ]
