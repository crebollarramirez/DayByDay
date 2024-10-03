from django.http import JsonResponse
from boto3.dynamodb.conditions import Attr
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import UserManager  # Import the UserManager


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Call UserManager to validate the login
        user_manager = UserManager()
        result = user_manager.login(username, password)

        if result["success"]:
            return Response({"message": result["message"]}, status=status.HTTP_200_OK)
        else:
            return Response({"message": result["message"]}, status=status.HTTP_401_UNAUTHORIZED)
        