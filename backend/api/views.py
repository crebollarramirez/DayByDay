from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.ScheduleManager import ScheduleManager
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # This will create the user
            return Response({"username": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        return Response(str(self.request.user))
    


class TodosList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        # Retrieve the authenticated user
        user = self.request.user

        # Assuming get_user_schedule is a method in your ScheduleManager
        return Response(ScheduleManager.getTodos(self.request, kwargs["date"]))

    def post(self, request, *args, **kwargs) -> Response:
        data = request.data

        # All items have this information 
        item_type = data.get("item_type")
        content = data.get("content")
        completed = data.get("completed")
        date = data.get("date")
        title = data.get("title")
        timeFrame = data.get("timeFrame")
        user_id = str(self.request.user)

        return ScheduleManager.create(
            user_id=user_id, 
            item_type=item_type,
            content=content, 
            completed=completed,
            date=date, 
            title=title,
            timeFrame=timeFrame
        )

    def delete(self, request, *args, **kwargs) -> Response:
        user = str(self.request.user)

        response = ScheduleManager.delete(
            request, kwargs["item_id"], kwargs["item_type"]
        )
        return response

    def put(self, request, *args, **kwargs) -> Response:
        user = str(self.request.user)

        response = ScheduleManager.update(
            request, kwargs["item_id"], kwargs["item_type"]
        )
        return response


class AllStatusChange(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs) -> Response:
        user = str(self.request.user)

        response = ScheduleManager.changeStatus(
            request, kwargs["item_id"], kwargs["item_type"]
        )
        return response


class WeekList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        print(kwargs["date"])

        user = self.request.user

        return Response(ScheduleManager.getWeek(self.request, kwargs["date"]))


class TaskList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        return Response(ScheduleManager.getTasks(self.request))

    def post(self, request, *args, **kwargs) -> Response:
        data = request.data

        # All items have this information 
        item_type = data.get("item_type")
        content = data.get("content")
        completed = data.get("completed")
        date = data.get("date")
        title = data.get("title")
        timeFrame = data.get("timeFrame")
        user_id = str(self.request.user)
        
        return ScheduleManager.create(
            user_id=user_id, 
            item_type=item_type,
            content=content, 
            completed=completed,
            date=date, 
            title=title,
            timeFrame=timeFrame
        )


    def put(self, request, *args, **kwargs) -> Response:
        return ScheduleManager.update(
            self.request, kwargs["item_id"], kwargs["item_type"]
        )

    def delete(self, request, *args, **kwargs) -> Response:
        return ScheduleManager.delete(
            self.request, kwargs["item_id"], kwargs["item_type"]
        )


class TodayList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        response = ScheduleManager.getToday(request, kwargs["todayDate"])
        return Response(response)