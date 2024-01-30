from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import FamilyMemberSerializer, ParentListSerializer, NewSerializer
from .models import Family_Member


class FamilyMemberListView(generics.ListAPIView):
    """Retrieves a list of all family members"""
    queryset = Family_Member.objects.all()
    serializer_class = NewSerializer
    serializer_class = FamilyMemberSerializer


class FamilyMemberUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves updates and delets a member"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer


class ParentListView(generics.ListAPIView):
    """Retrieves a list of all parents"""
    queryset = Family_Member.objects.all()
    serializer_class = ParentListSerializer


class CreateFamilyMember(APIView):
    def post(self, request, format=None):
        serializer = NewSerializer(data=request.data)
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
    """Searches for a member by name"""
    def get(self, request, format=None):
        member_id = request.query_params.get('member_id', None)
        if member_id is not None:
            try:
                member = Family_Member.objects.get(id=member_id)
                if member.parents.count() > 0:
                    parents_serializer = ParentListSerializer(member.parents.all(), many=True)
                    return Response(parents_serializer.data)
                else:
                    return Response({
                        "parents": None
                        })
            except Family_Member.DoesNotExist:
                return Response({'error': 'Family member not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Member name is required.'}, status=status.HTTP_400_BAD_REQUEST)

