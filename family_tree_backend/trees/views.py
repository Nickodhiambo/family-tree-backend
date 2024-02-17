from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.urls import reverse
from .serializers import FamilyMemberSerializer, CreateMemberSerializer, ParentSerializer
from .models import Family_Member


class FamilyMemberListView(generics.ListAPIView):
    """Retrieves a list of all family members"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer


class FamilyMemberUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves updates and delets a member"""
    queryset = Family_Member.objects.all()
    serializer_class = CreateMemberSerializer

    def put(self, request, pk, format=None):
        member = Family_Member.objects.get(pk=pk)
        serializer = CreateMemberSerializer(member, data=request.data)
        if serializer.is_valid():
            # Extract children from the data
            children_data = serializer.validated_data.pop('children', [])
            # Create the member
            member = serializer.save()
            # Create parent-child relationships
            for child_name in (children_data):
                child = Family_Member.objects.create(name=child_name)
                member.child = child
                member.save()
                member = child  # Move to the next level in the hierarchy
            response = HttpResponseRedirect(reverse('trees:family-member-single', kwargs={'pk': pk}))
            return response


class CreateFamilyMember(APIView):
    def post(self, request, format=None):
        serializer = CreateMemberSerializer(data=request.data)
        if serializer.is_valid():
            # Extract children from the data
            children_data = serializer.validated_data.pop('children', [])
            # Create the member
            member = serializer.save()
            # Create parent-child relationships
            for child_name in (children_data):
                child = Family_Member.objects.create(name=child_name)
                member.child = child
                member.save()
                member = child  # Move to the next level in the hierarchy
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchFamilyMember(APIView):
    def get(self, request, member_id):
        try:
            member = Family_Member.objects.get(id=member_id)
        except Family_Member.DoesNotExist:
            return Response({"error": "Family Member not found"}, status=status.HTTP_404_NOT_FOUND)

        parents_chain = member.get_parents_chain(member)

        serializer = ParentSerializer(parents_chain, many=True)

        return Response(serializer.data)

class FamilyMemberSingleView(generics.RetrieveUpdateAPIView):
    """Retrieves a single member"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
