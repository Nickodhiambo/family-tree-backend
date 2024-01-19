from django.shortcuts import render, redirect
from .models import Family_Member
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import FamilyMemberSerializer, ParentListSerializer, NewSerializer
from .permissions import IsAdminUser
from django.core.files.base import ContentFile
import cv2
import os
from django.conf import settings

# Create your views here.

class FamilyMemberCreateView(generics.CreateAPIView):
    """Creates a family member"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
   # permission_classes = [IsAdminUser]

class FamilyMemberListView(generics.ListAPIView):
    """Retrieves a list of all family members"""
    queryset = Family_Member.objects.all()
    serializer_class = NewSerializer
    #permission_classes = [IsAdminUser]

class FamilyMemberParentsView(generics.RetrieveAPIView):
    """Retrieves a member object with parents"""
    queryset = Family_Member.objects.all()
    serializer_class = FamilyMemberSerializer
    #permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """Retrieves a member with parents and children"""
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
    serializer_class = NewSerializer

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

class ParentListView(generics.ListAPIView):
    """Retrieves a list of all parents"""
    queryset = Family_Member.objects.all()
    serializer_class = ParentListSerializer

class CreateFamilyMember(APIView):
    def post(self, request, format=None):
        serializer = NewSerializer(data=request.data)

        if serializer.is_valid():
            # Extract parents from the data
            parents_data = serializer.validated_data.pop('parents', [])

            # Create the member
            member = serializer.save()

            # Create parent-child relationships
            for parent_name in (parents_data):
                parent = Family_Member.objects.create(user_name=parent_name)
                member.parent = parent
                member.save()
                member = parent  # Move to the next level in the hierarchy

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchFamilyMember(APIView):
    """Searches for a member by name"""
    def get(self, request, format=None):
        member_id = request.query_params.get('member_id', None)

        if member_id is not None:
            try:
                member = Family_Member.objects.get(id=member_id)
                family_tree = member.get_family_tree()
                serializer = NewSerializer(family_tree, many=True)
                return Response(serializer.data)
            except Family_Member.DoesNotExist:
                return Response({'error': 'Family member not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Member name is required.'}, status=status.HTTP_400_BAD_REQUEST)

# Load the template certificate image (save it in the static folder)
template_image = cv2.imread(os.path.join(settings.MEDIA_ROOT, 'template.png'))

# Function to update the image with text
def update_certificate_template(template_image, user_name):
    # Make a copy of the template to work on
    template = template_image.copy()
    coords = (x,y) # Replace with coordinate of where to update

	# Define the font, color, and size for the text to be added
    font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    font_color = (0, 0, 0)  # Black color (BGR format)
    font_scale = 1
    thickness = 1
    line_type = cv2.LINE_AA

	# Put the user's name at the specified coordinates
    cv2.putText(template, user_name, coords, font, font_scale, font_color, thickness, lineType=line_type)

    return template

# View for generating and updating certificates
def generate_certificate(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']

        updated_template = update_certificate_template(template_image, user_name)

        # Convert the updated image to a format suitable for saving
        ret, buf = cv2.imencode('.png', updated_template)
        image = ContentFile(buf.tobytes())

        certificate = Family_Member(user_name=user_name)
        certificate.certificate_image.save(f"{user_name}.png", image)
        certificate.save()

        return redirect('certificate_display', id=certificate.id)
    else:
        return render(request, 'trees/certificate-form.html')

# View for displaying the updated certificate
def certificate_display(request, id):
    certificate = Family_Member.objects.get(id=id)
    return render(request, 'trees/certificate-display.html', {'certificate': certificate})
	
