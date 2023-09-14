from django.shortcuts import render
from .models import Family_Member
from rest_framework import generics
from .serializers import FamilyMemberSerializer
from .permissions import IsAdminUser

# Create your views here.

class FamilyMemberCreateView(generics.CreateAPIView):
    """Creates a family member"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAdminUser]

class FamilyMemberListView(generics.ListAPIView):
    """Retrieves a list of all family members"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAdminUser]

class FamilyMemberSingleView(generics.RetrieveAPIView):
    """Retrieves a single member from database"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAdminUser]

class FamilyMemberUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves updates and delets a member"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAdminUser]
