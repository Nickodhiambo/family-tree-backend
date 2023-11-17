from django.shortcuts import render
from .models import Family_Member
from rest_framework import generics
from rest_framework.response import Response
from .serializers import FamilyMemberSerializer
from .permissions import IsAdminUser

# Create your views here.

class FamilyMemberCreateView(generics.CreateAPIView):
    """Creates a family member"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
   # permission_classes = [IsAdminUser]

class FamilyMemberListView(generics.ListAPIView):
    """Retrieves a list of all family members"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
    #permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Customizing the response format
        formatted_data = {"members": serializer.data}

        return Response({"data": formatted_data})

class FamilyMemberParentsView(generics.RetrieveAPIView):
    """Retrieves a member object with parents"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
    #permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a member with parents and children"""
        instance = self.get_object()

        if instance:
            # Create a list to store parents to the member, including the member
            parent_tree = instance.get_family_tree()
            return Response({
                "parent_tree": FamilyMemberSerializer(parent_tree, many=True).data
                })
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class FamilyMemberChildrenView(generics.RetrieveAPIView):
    """Retrieves a member's children"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer

    def retrieve(self, request, *args, **kwargs):
        # Get a member object
        instance = self.get_object()

        if instance:
            # Check if a member has children and return children list
            if instance.children.count() > 0:
                children_serializer = FamilyMemberSerializer(instance.children.all(), many=True)
                return Response({
                    "children": children_serializer.data
                    })
            else:
                return Response({
                    "children": None
                    })
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class FamilyMemberUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves updates and delets a member"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
    #permission_classes = [IsAdminUser]
