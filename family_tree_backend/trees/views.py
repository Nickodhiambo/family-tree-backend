from django.shortcuts import render
from .models import Family_Member
from rest_framework import generics
from rest_framework.response import Response
from .serializers import FamilyMemberSerializer
from .permissions import IsAdminUser
from django.template import loader
import cv2

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
    template_name = 'certificate_template.html'

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a member with parents and children
        """
        instance = self.get_object()

        if instance:
            # Create a list to store parents to the member, including the member
            parent_tree = instance.get_family_tree()

            # Load certificate image from database
            certificate_img_path = instance.certificate_image.path
            certificate_img = cv2.imread(certificate_img_path)

            ## Display the image and capture coordinates
    
            # Display loaded cert image
            cv2.imshow('Certificate Image', certificate_img)
    
            # Detects user's mouse events
            cv2.setMouseCallback('Certificate Image', self.get_coordinates_callback)
    
            # Waits indefinitely for user to press a key
            cv2.waitKey(0)
    
            #Closes the cert image window
            cv2.destroyAllWindows()

            # Update the model with captured coordinates
            instance.data_coordinates = self.coordinates
            instance.save()

            # Render the cert using a template
            template = loader.get_template(self.template_name)
            context = {
                    'member': instance,
                    'parent_tree': parent_tree,
                    'image_url': instance.certificate_image.url if instance.certificate_image else None
                    }
            rendered_certificate = template.render(context)
            return HttpResponse(rendered_certificate)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_coordinates_callback(self):
        """Captures coordinates from user input"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.coordinates = f'{x}, {y}'
            print(f'Clicked at coordinates: {self.coordinates}')

    """def retrieve(self, request, *args, **kwargs):
        Retrieves a member with parents and children
        instance = self.get_object()

        if instance:
            # Create a list to store parents to the member, including the member
            parent_tree = instance.get_family_tree()
            return Response({
                "parent_tree": FamilyMemberSerializer(parent_tree, many=True).data
                })
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)"""

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
