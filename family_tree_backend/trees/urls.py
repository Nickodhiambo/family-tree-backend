"""Define urls for trees"""

from django.urls import path
from . import views

app_name = 'trees'

urlpatterns = [
        #Create a member
        path('api/create-member/', views.FamilyMemberCreateView.as_view(), name='family-member-create'),

        #Retrieves a list of all members
        path('api/view-list/', views.FamilyMemberListView.as_view(), name='family-member-list'),

        #Retrieves a single member
        path('api/view-single/<int:pk>/', views.FamilyMemberSingleView.as_view(), name='family-member-single'),

        #Retrieve, update, delete a single member
        path('api/update-delete/<int:pk>/', views.FamilyMemberUpdateDeleteView.as_view(), name='family-member-update-delete')
]
