from rest_framework.response import Response
import json
from django.conf import settings
from ..models.models import FrequentTask, Goal
from ..models.UserData_model import UserData
from ..models.Todo_Model import Todo
from ..models.Task_Model import Task
from boto3.dynamodb.conditions import Key, Attr
import uuid


class ScheduleManager:

    # type: boto3.resources.factory.dynamodb.Table
    # description: The DynamoDB table object
    __table = settings.TABLE

    @classmethod
    def getTodos(cls, user_id, date) -> dict:
        """
        Gets the todos for the user given the date.

        Args:
            user_id (str): The user ID of the user for whom to get the todos.
            date (str): The date for which to get the todos.

        Returns:
            A dictionary where the keys are the dates and the values are dictionaries
            that contain the tasks for each date.
        """
        todos = []

        # Getting all user todos
        try:
            response = cls.__table.query(
                IndexName="ItemTypeIndex",
                KeyConditionExpression=Key('user_id').eq(user_id) & Key('item_type').eq('TODO')
            )

        # Filter the todos by date

            todos = [todo for todo in response.get("Items", []) if todo.get("date") == date]

        except Exception as e:
            print(f"Error with fetching calendar data: {e}")
        
        return todos


    @classmethod
    def create_todo(cls, user_id, todoInfo) -> Response:
        """
        Creates a new TODO item for the specified user.

        Args:
            user_id (str): The ID of the user creating the TODO item.
            todoInfo (dict): A dictionary containing the details of the TODO item.
                - content (str): The content or description of the TODO item.
                - date (str): The date for which the TODO item is scheduled.

        Returns:
            Response: A Response object indicating the result of the operation.
                - 201 Created: If the TODO item was successfully created.
                - 400 Bad Request: If there was an error creating the TODO item.
        """
        
        # Creating a uuid for the item
        item_id = str(uuid.uuid4())

        try:
            cls.__table.put_item(
                Item={
                    "user_id": user_id,
                    "item_id": item_id,
                    "completed": False,
                    "item_type": "TODO",
                    "content": todoInfo["content"],
                    "date": todoInfo["date"],
                }
            )     
        except Exception as e:
            return Response({"message": "Todo was not created"}, status=400)
        
        return Response({"message": "Todo Created"}, status=201)