from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import Family_Member_Serializer, Ancestors_Serializer, Base_Serializer
from .models import Family_Member


class CreateMemberView(generics.CreateAPIView):
    """Processes member creation action"""
    queryset = Family_Member.objects.all()
    serializer_class = Base_Serializer

    def perform_create(self, serializer):
        """Overrides the built-in perform create to pass a parent and member
        to a member instance
        """
        parent_id = self.request.data.get('parent')

        # Create the member
        instance = serializer.save()

        # Link a parent
        if parent_id:
            parent = Family_Member.objects.get(id=parent_id)
            instance.parent = parent
            instance.save()

       # Link a child
        child_id = self.request.data.get('children')
        if child_id:
            child = Family_Member.objects.get(id=child_id)
            instance.children.add(child) 


class UpdateDeleteMemberView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, and Updates or Destroys a Member"""
    queryset = Family_Member.objects.all()
    serializer_class = Base_Serializer


class ListView(generics.ListAPIView):
    """Retrieves a list of all members"""
    queryset = Family_Member.objects.all()
    serializer_class = Family_Member_Serializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Customizing the response format
        return Response({"data": serializer.data})


class SearchMemberView(generics.RetrieveAPIView):
    """Searches for a member"""
    queryset = Family_Member.objects.all()
    serializer_class = Ancestors_Serializer

    def retrieve(self, request, *args, **kwargs):
        """Retrieves a member based on the parameters passed in the URL.
        Overrides default retrieve method"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
