from boto3.dynamodb.conditions import Attr
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ScheduleManager  # Import the UserManager
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserSerializer, TodoSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class TodosList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve the authenticated user
        user = self.request.user
        user_id = user.id

        # Assuming get_user_schedule is a method in your ScheduleManager
        return ScheduleManager.getTodos(self.request, user_id)
        
    def perform_create(self, request):
        user = request.user
        user_id = user.id
        title = request.data.get('title')
        content = request.data.get('content')
        completed = False

        ScheduleManager.create()
        
