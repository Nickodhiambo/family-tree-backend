"""Define urls for trees"""

from django.urls import path
from . import views

app_name = 'trees'

urlpatterns = [
        # Update/delete a member
        path('api/update_member/<int:pk>/', views.FamilyMemberUpdateDeleteView.as_view(), name='update-member'),

        # View members' list
        path('api/view_list/', views.FamilyMemberListView.as_view(), name='view-list'),

		# New create endpoint
        path('api/create_family_member/', views.CreateFamilyMember.as_view(), name='create_family_member'),

        # New search member endpoint
        path('api/search_family_member/', views.SearchFamilyMember.as_view(), name='search_family_member')
        ]

