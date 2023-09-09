"""Define urls for trees"""

from django.urls import path
from . import views

app_name = 'trees'

urlpatterns = [
        #Index page
        path('home/', views.index, name='index'),

        #Create a member
        path('create/', views.create_member, name='create_member'),

        #Search for member
        path('search/', views.search_member, name='search_member'),
]
