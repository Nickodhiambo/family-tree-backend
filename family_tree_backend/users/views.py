from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import PasswordResetView
from django.http import HttpRequest
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
import os

# Create your views here.

class login_view(APIView):
    """Logs in a user"""

    authentication_classes = [JWTAuthentication]

    def post(self, request):
        target_email = os.environ.get('TARGET_EMAIL')
        email = request.data.get('email')
        password = request.data.get('password')

        if email != target_email:
            return Response({'error': 'Invalid email'}, status=status.HTTP_401_UNAUTHORIZED)
        user = authenticate(request, email=email, password=password)


        if user is not None:
            login(request, user)
            # Generate Access Token and Refresh Token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            #jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            #jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            #payload = jwt_payload_handler(user)
            #token = jwt_encode_handler(payload)
            return Response({'access_token': access_token, 'refresh_token': refresh_token})

        elif user is not None and not user.is_active:
            return Response({'error': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class TokenRefreshViewCustom(TokenRefreshView):
    """Generates a new access token"""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class logout_view(APIView):
    """Processes logout request"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        #Invalidate the user's token
        user = request.user
        user.auth_token.delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)

"""
class CustomPasswordResetView(APIView):
    Allows a user to reset their password
    def post(self, request):
        # Extract the user's email from request data
        email = request.data.get('email')

        # Create a Http request object to pass the email to the view class
        #password_reset_request = HttpRequest()
        #password_reset_request.POST = {'email': email}
        request._request = request
        request.POST = request.data

        # Make an instance of password reset
        password_reset_view = PasswordResetView.as_view()

        # Call password reset view with a new request object
        response = password_reset_view(request)

        #Check response status and return a message
        if response.status_code == 302: # Successful redirect to password reset done page
            return response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
        else:
            return response({'message': 'Password reset request failed'}, status=status.HTTP_400_BAD_REQUEST)
            """
