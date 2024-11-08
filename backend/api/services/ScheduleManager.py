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
    """
    Private Class Member Variables
    """

    # type: dict[str, UserData]
    # description: A dictionary to store all the users data
    #              The key is the user_id and the value is the UserData object
    __users: dict[str, UserData] = {}

    # type: boto3.resources.factory.dynamodb.Table
    # description: The DynamoDB table object
    __table = settings.TABLE


    """
    Fetches and organizes user data from the DynamoDB table.

    This method scans the DynamoDB table to retrieve all items, which
    are then processed and organized into user-specific data structures.
    For each item retrieved, it determines the user ID, item type, and other
    attributes, and stores them appropriately in the `__users` dictionary.
    The item type can be either "TODO" or "TASK", and the method creates
    and adds the corresponding Todo or Task object to the user's data.

    Raises:
        Exception: If there is an error while fetching data from the database.
    """
    @classmethod
    def getData(cls) -> None:
        try:
            response = cls.__table.scan()
            items = response.get("Items", [])

            for item in items:
                # Getting the data from database DYNAMODB
                user_id, item_type = item.get("user#item_type").split("#")
                user_id = str(user_id)
                date = item.get("date")

                _, item_id = item.get("user#item_id").split("#")
                content = item.get("content")
                isCompleted = item.get("completed")

                if user_id not in cls.__users:
                    cls.__users[user_id] = UserData(user_id)

                # Now setting the data to the correct user and correct type of data
                if item_type == "TODO":
                    todo = Todo(item_id, content, isCompleted, date)
                    cls.__users[user_id].add_todo(todo)

                elif item_type == "TASK":
                    title = item.get("title")
                    timeFrame = item.get("timeFrame")

                    task = Task(item_id, title, content, isCompleted, timeFrame, date)
                    cls.__users[user_id].add_task(task, True)

        except Exception as e:
            print(f"Error with fetching calendar data: {e}")

    """
    Gets the tasks for the given week and date.

    Args:
        request: The request object from the view.
        date: The date for which we want to get the tasks and todos.

    Returns:
        A dictionary where the keys are the days of the week and the values are
        dictionaries that contain the tasks for each day.
    """
    @classmethod
    def getWeek(cls, request, date) -> dict:
        user_id = str(request.user)

        if user_id not in cls.__users:
            cls.__users[user_id] = UserData(user_id)

        return cls.__users[user_id].getWeek(date)

       

    @classmethod
    def getToday(cls, request, date) -> dict:
        if request.method == "GET":
            user_id = str(request.user)

            if user_id not in cls.__users:
                cls.__users[user_id] = UserData(user_id)

            return cls.__users[user_id].getToday(date)


    """
    Gets the tasks for the user.

    Args:
        request: The request object from the view.

    Returns:
        A dictionary where the keys are the dates and the values are dictionaries
        that contain the tasks for each date.
    """
    @classmethod
    def getTasks(cls, request) -> dict[str, dict]:
        user_id = str(request.user)

        if user_id not in cls.__users:
            cls.__users[user_id] = UserData(user_id)

        return cls.__users[user_id].get_tasks()

    @classmethod
    def getCustomizedWeek(cls):
        pass

    @classmethod
    def getTodos(cls, request, date) -> dict:
        user_id = str(request.user)

        if user_id not in cls.__users:
            cls.__users[user_id] = UserData(user_id)

        return cls.__users[user_id].get_todos(date)

    def getGoals(cls, request) -> None:
        if request.method == "GET":
            pass
    
    """
    Creates a new task or todo for the given user.

    Args:
        user_id (str): The user ID of the user for whom to create the task or todo.
        item_type (str): The type of item to create, either "TODO" or "TASK".
        content (str): The content of the task or todo.
        completed (bool): A flag indicating whether the task or todo is completed.
        date (str): The date for which the task or todo is scheduled.
        timeFrame (list): A list of two strings in the format "HH:MM" representing the start and end times of the task or todo.
        title (str): The title of the task or todo.

    Returns:
        A Response object with a message indicating whether the task or todo was created successfully.
    """
    @classmethod
    def create(
        cls,
        user_id: str = None,
        item_type: str = None,
        content: str = None,
        completed: bool = None,
        date: str = None,
        timeFrame: list = None,
        title: str = None,
    ) -> Response:

        if user_id not in cls.__users:
            cls.__users[user_id] = UserData(user_id)

        # Creating a uuid for the item
        item_id = str(uuid.uuid4())

        if item_type == "TODO":
            cls.__users[user_id].add_todo(
                Todo(item_id=item_id, date=date, content=content, completed=completed)
            )
            cls.__table.put_item(
                Item={
                    "user#item_type": "#".join([user_id, item_type]),
                    "user#item_id": "#".join([user_id, item_id]),
                    "content": content,
                    "completed": completed,
                    "date": date,
                }
            )
        elif item_type == "TASK":
            task = Task(
                item_id=item_id,
                title=title,
                content=content,
                completed=completed,
                timeFrame=timeFrame,
                date=date,
            )

            if cls.time_frame_overlap(user_id, task, date):
                return Response({"message": "Task was not created"}, status=400)

            if cls.__users[user_id].add_task(task):
                response = cls.__table.put_item(
                    Item={
                        "user#item_type": "#".join([user_id, item_type]),
                        "user#item_id": "#".join([user_id, item_id]),
                        "content": content,
                        "completed": completed,
                        "timeFrame": timeFrame,
                        "date": date,
                        "title": title,
                    }
                )
            else:
                return Response({"message": "Task was not created"}, status=400)
        return Response({"message": "Task Created"}, status=201)


    """
    Deletes a task or todo item for the given user.

    Args:
        request: The request object from the view.
        item_id (str): The ID of the item to delete.
        item_type (str): The type of item to delete, either "TODO", "TASK", or "FREQUENT".

    Returns:
        A Response object with a message indicating whether the item was deleted successfully.
    """
    @classmethod
    def delete(cls, request, item_id, item_type) -> Response:
        user_id = str(request.user)
        if request.method == "DELETE":
            if item_type == "TODO":
                cls.__users[user_id].delete_todo(item_id)

                response = cls.__table.delete_item(
                    Key={
                        "user#item_type": "#".join([user_id, item_type]),
                        "user#item_id": "#".join([user_id, item_id]),
                    }
                )

                return Response({"message": "Todo deleted successfully."}, status=204)

            elif item_type == "TASK":
                cls.__users[user_id].delete_task(item_id)
                cls.__table.delete_item(
                    Key={
                        "user#item_type": "#".join([user_id, item_type]),
                        "user#item_id": "#".join([user_id, item_id]),
                    }
                )

                return Response({"message": "Todo deleted successfully."}, status=204)

            elif item_type == "FREQUENT":
                cls.__users[user_id].delete_frequentTask(item_id)

                cls.__table.delete_item(
                    Key={
                        "user#item_type": "#".join([user_id, item_type]),
                        "user#item_id": "#".join([user_id, item_id]),
                    }
                )

                return Response({"message": "Todo deleted successfully."}, status=204)

    """
    Updates an existing item of a given type.

    Args:
        request (Request): The request containing the data to update the item.
        item_id (str): The ID of the item to update.
        item_type (str): The type of item to update. Must be one of "TODO", "TASK", or "FREQUENT".

    Returns:
        Response: A response containing the updated item data.
    """
    @classmethod
    def update(cls, request, item_id, item_type) -> Response:

        user_id = str(request.user)
        if request.method == "PUT":
            data = json.loads(request.body)
            content = data.get("content")
            completed = data.get("completed")
            date = data.get("completed")

            if item_type == "TODO":
                cls.__users[user_id].update_todo(
                    item_id, isCompleted=completed, content=content
                )

                response = cls.__table.update_item(
                    Key={
                        "user#item_id": user_id + "#" + item_id,
                        "user#item_type": user_id + "#" + item_type,
                    },
                    UpdateExpression="SET content = :c, completed = :k",
                    ExpressionAttributeValues={":c": content, ":k": completed},
                    ReturnValues="UPDATED_NEW",
                )

                return Response(
                    {
                        "message": "Todo updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )

            elif item_type == "TASK":
                title = data.get("title")
                timeFrame = data.get("timeFrame")

                cls.__users[user_id].update_task(
                    item_id,
                    title=title,
                    content=content,
                    timeFrame=timeFrame,
                    date=date,
                )
                response = cls.__table.update_item(
                    Key={
                        "user#item_id": user_id + "#" + item_id,
                        "user#item_type": user_id + "#" + item_type,
                    },
                    UpdateExpression="SET title = :t, content = :c, timeFrame = :tf, #d = :d",
                    ExpressionAttributeValues={
                        ":t": title,
                        ":c": content,
                        ":tf": timeFrame,
                        ":d": date,
                    },
                    ExpressionAttributeNames={
                        "#d": "date"  # 'date' is a reserved keyword in DynamoDB, so you need to use ExpressionAttributeNames to avoid conflicts
                    },
                    ReturnValues="UPDATED_NEW",
                )
            elif item_type == "FREQUENT":
                title = data.get("title")
                frequency = data.get("frequency")
                timeFrame = data.get("timeFrame")
                endFrequency = data.get("endFrequency")

                cls.__users[user_id].update_frequentTask(
                    item_id,
                    title=title,
                    frequency=frequency,
                    timeFrame=timeFrame,
                    endFrequency=endFrequency,
                )

    @classmethod
    def changeStatus(cls, request, item_id, item_type) -> Response:
        user_id = str(request.user)
        if request.method == "PUT":
            newStatus = bool(json.loads(request.body).get("completed"))

            if item_type == "TODO":
                cls.__users[user_id].update_todo(item_id, isCompleted=newStatus)

                response = cls.__table.update_item(
                    Key={
                        "user#item_id": user_id + "#" + item_id,
                        "user#item_type": user_id + "#" + item_type,
                    },
                    UpdateExpression="set completed = :c",
                    ExpressionAttributeValues={":c": newStatus},
                    ReturnValues="UPDATED_NEW",
                )

                return Response(
                    {
                        "message": "Todo status updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )
            elif item_type == "TASK":
                cls.__users[user_id].update_task(item_id, isCompleted=newStatus)
                response = cls.__table.update_item(
                    Key={
                        "user#item_id": user_id + "#" + item_id,
                        "user#item_type": user_id + "#" + item_type,
                    },
                    UpdateExpression="set completed = :c",
                    ExpressionAttributeValues={":c": newStatus},
                    ReturnValues="UPDATED_NEW",
                )

                return Response(
                    {
                        "message": "Task status updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )

    """
    Check if two tasks overlap based on their time frames.

    :param task: timeFrame in format ["HH:MM", "HH:MM"], date in format MM-DD-YYYY
    :return: a Task if there was an overlap, else None
    """

    @classmethod
    def time_frame_overlap(cls, user_id: str, task: Task, date: str) -> tuple | None:
        # Convert military time to minutes since midnight for comparison
        def military_to_minutes(military_time):
            hours, minutes = map(int, military_time.split(":"))
            return hours * 60 + minutes

        user = cls.__users.get(user_id)

        # If the user or the task date doesn't exist, return None
        if not user or date not in user.get_tasks():
            return None

        # Iterate through existing tasks on the same date
        overlap_tasks = []
        for event in user.get_tasks()[date].values():
            start1, end1 = task.timeFrame
            start2, end2 = event["timeFrame"]

            # Convert timeframes to minutes for comparison
            start1_minutes = military_to_minutes(start1)
            end1_minutes = military_to_minutes(end1)
            start2_minutes = military_to_minutes(start2)
            end2_minutes = military_to_minutes(end2)

            # Check if the timeframes overlap
            if not (end1_minutes <= start2_minutes or end2_minutes <= start1_minutes):
                overlap_tasks.append(event)  # Add the task that overlaps to the list

        # Return the list of tasks that overlap, or None if no overlap is found
        return tuple(overlap_tasks) if overlap_tasks else None
    
    @classmethod
    def get_user(cls, user_id: str) -> UserData:
        return cls.__users.get(user_id)
