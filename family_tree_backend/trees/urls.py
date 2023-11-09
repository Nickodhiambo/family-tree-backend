"""Define urls for trees"""

from django.urls import path
from . import views

app_name = 'trees'

urlpatterns = [
        # Create a member
        path('api/create-member/', views.FamilyMemberCreateView.as_view(), name='family-member-create'),

        # Retrieves a list of all members
        path('api/view-list/', views.FamilyMemberListView.as_view(), name='family-member-list'),

        # Retrieves a member's parents
        path('api/view-parents/<int:pk>/', views.FamilyMemberParentsView.as_view(), name='family-member-parents'),

        # Retrieves a member's children
        path('api/view-children/<int:pk>/', views.FamilyMemberChildrenView.as_view(), name='family-member-children'),

        #Retrieve, update, delete a single member
        path('api/update-delete/<int:pk>/', views.FamilyMemberUpdateDeleteView.as_view(), name='family-member-update-delete')
]
