import boto3
from .models import *
from django.http import JsonResponse
import json
from django.conf import settings
from enum import Enum
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime


DAYS_OF_THE_WEEK = [
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
    "SUNDAY",
]


class ScheduleManager:

    # Private Class Member Variables
    __table = None
    __todos = {}
    __frequentTasks = {
        "MONDAY": {},
        "TUESDAY": {},
        "WEDNESDAY": {},
        "THURSDAY": {},
        "FRIDAY": {},
        "SATURDAY": {},
        "SUNDAY": {},
        "EVERYDAY": {},
        "BIWEEKLY": {},
        "MONTHLY": {},
        "YEARLY": {},
    }
    __tasks = {}
    __goals = {}

    # For displaying today and the week
    __today = ()
    __todayTasks = {}
    __week = {
        "MONDAY": {},
        "TUESDAY": {},
        "WEDNESDAY": {},
        "THURSDAY": {},
        "FRIDAY": {},
        "SATURDAY": {},
        "SUNDAY": {},
    }

    # modify this later so it returns a value depending if it was able to connect to the database
    @classmethod
    def __set_table(cls) -> None:
        cls.__table = boto3.resource(
            "dynamodb",
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url="http://localhost:8080",  # For local DynamoDB instance
        ).Table(settings.AWS_DYNAMODB_TABLE_NAME)

    @classmethod
    def __setTodayDate(cls) -> None:
        today = datetime.now()
        # Format date as "MM-DD-YYYY" and get weekday
        cls.__today = (today.strftime("%m-%d-%Y"), 3)  # today.weekday() % 7)

    @classmethod
    def __setUpWeek(cls) -> None:
        # This is what puts all the tasks for the week, including today
        for day in DAYS_OF_THE_WEEK:
            for title, task in cls.__frequentTasks[day].items():
                cls.__week[day][title] = task.toDict()

        # Reordering from today
        reordered_days = (
            DAYS_OF_THE_WEEK[cls.__today[1] :] + DAYS_OF_THE_WEEK[: cls.__today[1]]
        )

        cls.__week = {key: cls.__week[key] for key in reordered_days}

    @classmethod
    def getTodayDate(cls) -> tuple:
        cls.__setTodayDate()
        return cls.__today

    # this works well
    @classmethod
    def getData(cls) -> None:
        cls.__setTodayDate()
        cls.__set_table()
        try:
            response = cls.__table.scan()
            items = response.get("Items", [])

            for item in items:
                item_type = item.get("item_type")

                if item_type == "TODO":
                    cls.__todos[item["title"]] = Todo(
                        title=item["title"],
                        content=item["content"],
                        completed=item.get("completed", False),
                    )

                elif item_type == "FREQUENT":
                    cls.__frequentTasks[item["frequency"]][item["title"]] = (
                        FrequentTask(
                            title=item["title"],
                            content=item["content"],
                            frequency=item["frequency"],
                            completed=item.get("completed", False),
                            timeFrame=item.get("timeFrame"),
                        )
                    )
                elif item_type == "TASK":
                    cls.__tasks[item["title"]] = Task(
                        title=item["title"],
                        content=item["content"],
                        completed=item.get("completed", False),
                        timeFrame=item.get("timeFrame"),
                        date=item.get("date"),
                    )
                elif item_type == "GOAL":
                    cls.__frquencyTasks[item["title"]] = Goal(
                        title=item["title"],
                        content=item["content"],
                        completed=item.get("completed", False),
                        taskMap=item.get("tasksMap", {}),
                    )
        except Exception as e:
            print(f"Error with fetching data: {e}")

    @classmethod
    def getWeek(cls, request) -> JsonResponse:
        if request.method == "GET":

            # this is just to test the data
            test = {
                "MONDAY": {
                    "task1": {
                        "item_type": "FREQUENT",
                        "title": "Morning Walk",
                        "content": "Take the dog for a morning walk.",
                        "frequency": "MONDAY",
                        "completed": False,
                        "timeFrame": ("7:00AM", "8:00AM"),
                    },
                    "task2": {
                        "item_type": "FREQUENT",
                        "title": "Night Stuff",
                        "content": "go to sleep",
                        "frequency": "MONDAY",
                        "completed": False,
                        "timeFrame": ("10:00PM", "8:00AM"),
                    },
                },
                "TUESDAY": {
                    "task1": {
                        "item_type": "FREQUENT",
                        "title": "Grocery Shopping",
                        "content": "Buy groceries for the week.",
                        "frequency": "TUESDAY",
                        "completed": False,
                        "timeFrame": ("10:00AM", "11:00AM"),
                    },
                },
                "WEDNESDAY": {
                    "task1": {
                        "item_type": "FREQUENT",
                        "title": "Weekly Meeting",
                        "content": "Attend the project weekly meeting.",
                        "frequency": "WEDNESDAY",
                        "completed": False,
                        "timeFrame": ("2:00PM", "3:00PM"),
                    }
                },
                "THURSDAY": {
                    "task1": {
                        "item_type": "FREQUENT",
                        "title": "Weekly Meeting",
                        "content": "Attend the project weekly meeting.",
                        "frequency": "WEDNESDAY",
                        "completed": False,
                        "timeFrame": ("2:00PM", "3:00PM"),
                    }
                },
            }
            cls.__setUpWeek()

            # returning week starting after today
            return JsonResponse(dict(list(cls.__week.items())[1:]))

    # @classmethod
    # def __setToday(cls) -> None:

    @classmethod
    def getToday(cls, response) -> JsonResponse:
        if response.method == "GET":
            return JsonResponse(cls.__week[DAYS_OF_THE_WEEK[cls.__today[1]]])

    @classmethod
    def getCustomizedWeek(cls):
        pass

    @classmethod
    def getTodos(cls, request) -> JsonResponse:
        cls.__setUpWeek()
        if request.method == "GET":
            # Create a list of dictionaries for each Todo object
            todos_dict_list = [
                todo.to_dict() for todo in cls.__todos.values()
            ]  # Use to_dict()
            return JsonResponse(
                todos_dict_list, safe=False
            )  # Return list of dicts as JSON response

    def getGoals(cls, request) -> JsonResponse:
        if request.method == "GET":
            pass

    @classmethod
    @csrf_exempt
    def create(cls, request) -> JsonResponse:
        if request.method == "POST":
            data = json.loads(request.body)
            item_type = data.get("item_type")

            if item_type == "TODO":
                title = data.get("title")
                content = data.get("content")
                completed = data.get("completed")
                if title in cls.__todos:
                    return JsonResponse(
                        {"error": "Todo item with this title already exists"},
                        status=400,
                    )

                cls.__todos[title] = Todo(
                    title=title, content=content, completed=completed
                )

                response = cls.__table.put_item(
                    Item={
                        "item_type": "TODO",
                        "title": title,
                        "content": content,
                        "completed": completed,
                    }
                )
            elif item_type == "FREQUENT":
                title = data.get("title")
                content = data.get("content")
                frequency = data.get("frequency")
                completed = data.get("completed")
                timeFrame = data.get("timeFrame")

                if title in cls.__frequentTasks:
                    return JsonResponse(
                        {"error": "Frequent Task with this title already exists"},
                        status=400,
                    )

                cls.__frequentTasks[title] = FrequentTask(
                    title=title,
                    content=content,
                    frequency=frequency,
                    completed=completed,
                    timeFrame=timeFrame,
                )

                response = cls.__table.put_item(
                    Item={
                        "item_type": "FREQUENT",
                        "title": title,
                        "content": content,
                        "frequency": frequency,
                        "completed": completed,
                        "timeFrame": timeFrame,
                    }
                )

            elif item_type == "TASK":
                title = data.get("title")
                content = data.get("content")
                completed = data.get("completed")
                timeFrame = data.get("timeFrame")
                date = data.get("date")

                if title in cls.__tasks:
                    return JsonResponse(
                        {"error": "Task already exists"},
                        status=400,
                    )

                cls.__tasks[title] = Task(
                    title=title,
                    content=content,
                    completed=completed,
                    timeFrame=timeFrame,
                    date=date,
                )

                response = cls.__table.put_item(
                    Item={
                        "item_type": "FREQUENT",
                        "title": title,
                        "content": content,
                        "frequency": frequency,
                        "completed": completed,
                        "timeFrame": timeFrame,
                    }
                )

            return JsonResponse({"message": "Task Created", "data": data}, status=201)

    @classmethod
    @csrf_exempt
    def delete(cls, request, title, item_type) -> JsonResponse:
        if request.method == "DELETE":
            if item_type == "TODO" and title in cls.__todos:
                cls.__table.delete_item(Key={"title": title, "item_type": item_type})
                del cls.__todos[title]
                return JsonResponse(
                    {"message": "Todo deleted successfully."}, status=204
                )

    @classmethod
    @csrf_exempt
    def update(cls, request, title, item_type) -> JsonResponse:
        if request.method == "PUT":
            if item_type == "TODO":
                data = json.loads(request.body)
                newData = data.get("newData")
                response = cls.__table.update_item(
                    Key={"title": title, "item_type": item_type},
                    UpdateExpression="set content = :c",
                    ExpressionAttributeValues={":c": newData},
                    ReturnValues="UPDATED_NEW",
                )

                cls.__todos[title].content = newData
                return JsonResponse(
                    {
                        "message": "Todo updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )

    @classmethod
    @csrf_exempt
    def changeStatus(cls, request, title, item_type) -> JsonResponse:
        if request.method == "PUT":
            if item_type == "TODO":
                newStatus = json.loads(request.body)
                newStatus = newStatus.get('completed')
                response = cls.__table.update_item(
                    Key={"title": title, "item_type": item_type},
                    UpdateExpression="set completed = :c",
                    ExpressionAttributeValues={":c": newStatus},
                    ReturnValues="UPDATED_NEW",
                )

                cls.__todos[title].completed = bool(newStatus)
                return JsonResponse(
                    {
                        "message": "Todo status updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )
