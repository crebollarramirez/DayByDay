from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.ScheduleManager import ScheduleManager
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    API view to create a new user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new user.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A response object containing the username of the created user or errors if the request is invalid.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # This will create the user
            return Response({"username": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(APIView):
    """
    API view to retrieve information about the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request to retrieve user information.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A response object containing the username of the authenticated user.
        """
        return Response(str(self.request.user))


class Todos(APIView):
    """
    API view to handle todo items.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new todo item.

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A Response object with the result of the operation.

        Raises:
            HTTP_400_BAD_REQUEST: If the 'content' or 'date' fields are missing in the request data.
        """
        data = self.request.data

        if data.get("content") is None or data.get("item_date") is None:
            return Response(
                {"error": "Missing Field!"}, status=status.HTTP_400_BAD_REQUEST
            )

        return ScheduleManager.create_todo(str(self.request.user), data)

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handles GET requests to retrieve todos for a specific user and date.
        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Response: A Response object containing the todos for the specified user and date,
                      or an error message if an exception occurs.
        """

        try:
            todos = ScheduleManager.getTodos(
                str(self.request.user), request.query_params["date"]
            )
        except Exception as e:
            print("There was an internal error", e)
            return Response(
                {"error": "There was an internal error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(todos, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs) -> Response:
        """
        Handles DELETE requests to delete a todo item for a specific user and date.
        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Response: A Response object indicating the result of the delete operation.
        """

        if request.query_params["item_id"] is None:
            return Response(
                {"error": "Missing Field!"}, status=status.HTTP_400_BAD_REQUEST
            )

        return ScheduleManager.deleteTodo(
            str(self.request.user), request.query_params["item_id"]
        )

    def put(self, request, *args, **kwargs) -> Response:
        """
        Handles PUT requests to update a todo item for a specific user and date.
        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Response: A Response object indicating the result of the update operation.
        """
        if request.query_params["item_id"] is None:
            return Response(
                {"error": "Missing Field!"}, status=status.HTTP_400_BAD_REQUEST
            )

        return ScheduleManager.updateTodo(
            user_id=str(self.request.user),
            item_id=request.query_params["item_id"],
            completed=request.data.get("completed"),
            content=request.data.get("content"),
            date=request.data.get("item_date"),
        )
