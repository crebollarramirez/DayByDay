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

    def post(self, request, *args, **kwargs):
        print("New user created!")


class TodosList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        # Retrieve the authenticated user
        user = self.request.user
        print("This is the user is: " + str(user))

        # Assuming get_user_schedule is a method in your ScheduleManager
        return Response(ScheduleManager.getTodos(self.request))
    
    # def post(self, request, *args, **kwargs) -> Response:
    #     user = self.request.user
    #     # Handle POST request here
    #     print(f"Creating new task for user {user}")

    #     # Call the ScheduleManager create method
    #     response = ScheduleManager.create(request)

    #     return response

    def delete(self, request, *args, **kwargs) -> Response:
        user = str(self.request.user)
        
        print("we are delete a task for " + user)

        response = ScheduleManager.delete(request, kwargs['item_id'], kwargs['item_type'])
        return response
    
    def put(self, request, *args, **kwargs) -> Response:
        user = str(self.request.user)
        print("we are updating the task for " + user)

        response = ScheduleManager.update(request, kwargs['item_id'], kwargs['item_type'])
        return response

class AllStatusChange(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs) -> Response:
        user = str(self.request.user)

        response = ScheduleManager.changeStatus(request, kwargs['item_id'], kwargs['item_type'])
        return response
    
class WeekList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:    
        print(kwargs['date'])

        user = self.request.user

        return Response(ScheduleManager.getWeek(self.request, kwargs['date']))
    
    def delete(self, request, *args, **kwargs):
        user = str(self.request.user)
        
        print("we are delete a task for " + user)
        return ScheduleManager.delete(request, kwargs['item_id'], kwargs['item_type'])
    
    def post(self, request, *args, **kwargs) -> Response:
        return ScheduleManager.create(request)
    
    
class TodayList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        response = ScheduleManager.getToday(request, kwargs['todayDate'])
        return Response(response)
        
