from rest_framework.response import Response
import json
from django.conf import settings
from .models import FrequentTask, Goal
from .UserData_model import UserData
from .Todo_Model import Todo
from .Task_Model import Task
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr
import uuid

class ScheduleManager:
    __users: dict[str, UserData] = {}
    # Private Class Member Variables
    __table = settings.TABLE

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

    @classmethod
    def getWeek(cls, request, date) -> dict:
        user_id = str(request.user)

        if user_id not in cls.__users:
            cls.__users[user_id] = UserData(user_id)

        START_DAY = datetime.strptime(date, "%m-%d-%Y").date()
        week = {}

        user:UserData = cls.__users[user_id]

        for i in range(0, 5):
            dayName = str((START_DAY + timedelta(days=i)).strftime("%A"))
            fullDay = (
                dayName + ", " + str((START_DAY + timedelta(days=i)).strftime("%B %d"))
            )  # full Day name for the day
            d = str((START_DAY + timedelta(days=i)).strftime("%m-%d-%Y"))

            if dayName not in week:
                week[fullDay] = {}
            user:UserData = cls.__users[user_id]

            userTasks = user.get_tasks()
            if d in userTasks:
                week[fullDay] = userTasks[d]
        return week

    @classmethod
    def getToday(cls, request, date) -> dict:
        if request.method == "GET":
            user_id = str(request.user)

            if user_id not in cls.__users:
                cls.__users[user_id] = UserData(user_id)

            return cls.__users[user_id].getToday(date)

    @classmethod 
    def getTasks(cls, request) -> dict:
        if request.method == "GET":
            user_id = str(request.user)

        if user_id not in cls.__users:
            cls.__users[user_id] = UserData(user_id)   

        return cls.__users[user_id].get_tasks()
    @classmethod
    def getCustomizedWeek(cls):
        pass

    @classmethod
    def getTodos(cls, request, date) -> dict:
        if request.method == "GET":
            user_id = str(request.user)

            if user_id not in cls.__users:
                cls.__users[user_id] = UserData(user_id)

            return cls.__users[user_id].getTodos(date)

    def getGoals(cls, request) -> None:
        if request.method == "GET":
            pass

    @classmethod
    def create(cls, request) -> Response:
        user_id = str(request.user)

        if user_id not in cls.__users:
            cls.__users[user_id] = UserData(user_id)

        data = request.data

        # ALL ITEMS HAVE THESE ATTRIBUTES
        item_type = data.get("item_type")
        content = data.get("content")
        completed = data.get("completed")
        date = data.get("date")
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
            title = data.get("title")
            content = data.get("content")
            completed = data.get("completed")
            timeFrame = data.get("timeFrame")


            task = Task(
                item_id=item_id,
                title=title,
                content=content,
                completed=completed,
                timeFrame=timeFrame,
                date=date,
            )

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
        return Response({"message": "Task Created", "data": data}, status=201)

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

    @classmethod
    def update(cls, request, item_id, item_type) -> Response:
        user_id = str(request.user)
        if request.method == "PUT":
            data = json.loads(request.body)
            content = data.get("content")
            completed = data.get("completed")
            date = data.get("completed")

            if item_type == "TODO":
                cls.__users[user_id].update_todo(item_id, isCompleted=completed, content=content)

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
    def time_frame_overlap(cls, user_id, timeFrame, date) -> Task:
        # Convert military time to minutes since midnight for comparison
        def military_to_minutes(military_time):
            hours, minutes = map(int, military_time.split(":"))
            return hours * 60 + minutes

        user = cls.__users.get(user_id)

        # If the user or the task date doesn't exist, return None
        if not user or date not in user.get_tasks():
            return None

        # Iterate through existing tasks on the same date
        for event in user.get_tasks()[date]:
            start1, end1 = timeFrame
            start2, end2 = event.timeFrame

            # Convert timeframes to minutes for comparison
            start1_minutes = military_to_minutes(start1)
            end1_minutes = military_to_minutes(end1)
            start2_minutes = military_to_minutes(start2)
            end2_minutes = military_to_minutes(end2)

            # Check if the timeframes overlap
            if not (end1_minutes <= start2_minutes or end2_minutes <= start1_minutes):
                return event  # Return the task that overlaps

        # Return None if no overlap is found
        return None

