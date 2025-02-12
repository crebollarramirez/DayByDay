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
                KeyConditionExpression=Key("user_id").eq(user_id)
                & Key("item_type").eq("TODO"),
            )

            # Filter the todos by date

            todos = [
                todo for todo in response.get("Items", []) if todo.get("item_date") == date
            ]

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
                    "item_date": todoInfo["item_date"],
                }
            )
        except Exception as e:
            return Response({"message": "Todo was not created"}, status=400)

        return Response({"message": "Todo Created"}, status=201)

    @classmethod
    def deleteTodo(cls, user_id, item_id) -> Response:
        """
        Deletes a todo item from the DynamoDB table.

        Args:
            user_id (str): The ID of the user.
            item_id (str): The ID of the item to delete.

        Returns:
            Response: A response object indicating the result of the delete operation.
        """
        try:
            cls.__table.delete_item(
                Key={"user_id": user_id, "item_id": item_id},
                ConditionExpression="attribute_exists(item_id)",
            )

        except Exception as e:
            return Response({"message": "Todo was not deleted"}, status=400)

        return Response({"message": "Todo Deleted"}, status=200)

    @classmethod
    def updateTodo(
        cls, user_id, item_id, completed=None, content=None, date=None
    ) -> Response:
        """
        Updates a todo item in the DynamoDB table.

        Args:
            user_id (str): The ID of the user.
            item_id (str): The ID of the item to update.
            completed (str, optional): The completion status of the todo item ("True" or "False").
            content (str, optional): The content of the todo item.
            date (str, optional): The date of the todo item.

        Returns:
            Response: A response object indicating the result of the update operation.
        """
        
        if completed is None and content is None and date is None:
            return Response({"message": "Nothing to update"}, status=200)
        
        if completed is not None and completed not in ["True", "False"]:
            return Response({"message": "Invalid completed value needs to be True or False"}, status=400)

        try:
            update_expression = "SET "
            expression_attribute_values = {}

            if completed is not None:
                update_expression += "completed = :completed, "
                expression_attribute_values[":completed"] = (str(completed) == "True")

            if content is not None:
                update_expression += "content = :content, "
                expression_attribute_values[":content"] = content

            if date is not None:
                update_expression += "item_date = :item_date, "
                expression_attribute_values[":item_date"] = date

            # Remove the trailing comma and space
            update_expression = update_expression.rstrip(", ")
            cls.__table.update_item(
                Key={"user_id": user_id, "item_id": item_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
            )

        except Exception as e:
            print(e)
            return Response({"message": "Todo was not updated"}, status=400)

        return Response({"message": "Todo Updated"}, status=200)
