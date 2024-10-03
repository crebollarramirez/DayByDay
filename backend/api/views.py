from django.http import JsonResponse
from boto3.dynamodb.conditions import Attr
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import UserManager  # Import the UserManager
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Call UserManager to validate the login
        user = UserManager.authenticate_user(username, password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        return Response({"error": "Invalid credentials"}, status=400)

        
class CreateUserView(APIView):
    permission_classes = [AllowAny]
                      
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Call UserManager to handle the user registration
        result = UserManager().create_user(username, password)

        print(username)
        print(password)

        if result:
            return Response({"message": result}, status=status.HTTP_201_CREATED)
            
        return Response({"message": result}, status=status.HTTP_400_BAD_REQUEST)
        