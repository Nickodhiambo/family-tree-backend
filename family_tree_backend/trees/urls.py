"""Define urls for trees"""

from django.urls import path
from .views import CreateMemberView, UpdateDeleteMemberView, ListView, SearchMemberView

app_name = 'trees'

urlpatterns = [
        # Create member
        path('api/create_member/', CreateMemberView.as_view(), name='create-member'),

        # Update/delete a member
        path('api/update_member/<int:pk>/', UpdateDeleteMemberView.as_view(), name='update-member'),

        # View members' list
        path('api/view_list/', ListView.as_view(), name='view-list'),

        # Search for a member by id
        path('api/search_member/<int:pk>/', SearchMemberView.as_view(), name='search-member'),
        ]

