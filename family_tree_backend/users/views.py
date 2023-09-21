from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.

class login_view(APIView):
    """Logs in a user"""
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token})

        else:
            return Response({'error': 'Invalid credentials'}, status = status.HTTP_400_BAD_REQUEST)


class logout_view(APIView):
    """Processes logout request"""
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        #Invalidate the user's token
        user = request.user
        user.auth_token.delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)

def Custom_User(request):
    """Creates an admin user"""
    # Check if admin user already exists
    admin_user, created = User.objects.get_or_create(username='admin1')

    # If succesfully created, set additional attributes
    if created:
        admin_user.is_staff = True
        admin_user.is_superuser = True

        # Set the email address
        admin_user.email = 'nodhiambo01@gmail.com'

        admin_user.set_password('admin_password')
        admin_user.save()

        # Add user to admin group
        admin_user.groups.add(admin_group)
