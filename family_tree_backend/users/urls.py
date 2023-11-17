"""Defines URL patterns for users"""
from django.urls import path
from . import views

app_name='users'

urlpatterns = [
        # Admin login page
        path('api/login/', views.login_view.as_view(), name='login'),

        # Token reset
        path('token/refresh/', views.TokenRefreshViewCustom.as_view(), name='token_refresh'),

        # Admin logout
        path('api/logout/', views.logout_view.as_view(), name='logout'),

        # Password reset
        # path('password_reset/', views.CustomPasswordResetView.as_view(), name='password-reset')
        ]
