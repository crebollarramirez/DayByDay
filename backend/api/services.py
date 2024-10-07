import boto3
import boto3.dynamodb
from .models import *
from django.http import JsonResponse
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

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

    # key : id
    # value dict that holds all the todos
    __tasks = {}
    __goals = {}

    # For displaying today and the week
    __today = ()
    __todayTasks = {}
    __week = {}

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
        cls.__today = (today,  today.strftime("%m-%d-%Y"), today.strftime("%A"))
        print(cls.__today[2])

    @classmethod
    def __setUpTodayTasks(cls):
        cls.__todayTasks
        for title, task in cls.__frequentTasks[cls.__today[2].upper()].items():
            cls.__todayTasks[title] = task.toDict()

    @classmethod
    def __setUpWeek(cls) -> None:
        for i in range(1,7):
            day = str((cls.__today[0] + timedelta(days=i)).strftime("%A")).upper()
            if day not in cls.__week:
                cls.__week[day] = {}
            for title, task in cls.__frequentTasks[day.upper()].items():
                cls.__week[day][title] = task.toDict()


        cls.__setUpTodayTasks()
        print(cls.__week)


    @classmethod
    def __resetWeek(cls):
        cls.__week.clear()

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
                id, item_type = item.get("id#item_type").split('#')
                id = str(id)
                _ , title = item.get("id#title").split('#')

                cls.__todos[id] = {}
                if item_type == "TODO":
                    if id in cls.__todos:
                        cls.__todos[id][title] = Todo(
                            id=id,
                            title=title,
                            content=item["content"],
                            completed=item.get("completed", False),
                        )

                # elif item_type == "FREQUENT":
                #     cls.__frequentTasks[item["frequency"]][title] = (
                #         FrequentTask(
                #             title=title,
                #             content=item["content"],
                #             frequency=item["frequency"],
                #             completed=item.get("completed", False),
                #             timeFrame=item.get("timeFrame"),
                #         )
                #     )
                # elif item_type == "TASK":
                #     cls.__tasks[title] = Task(
                #         title=title,
                #         content=item["content"],
                #         completed=item.get("completed", False),
                #         timeFrame=item.get("timeFrame"),
                #         date=item.get("date"),
                #     )
                # elif item_type == "GOAL":
                #     cls.__frequencyTasks[title] = Goal(
                #         title=title,
                #         content=item["content"],
                #         completed=item.get("completed", False),
                #         taskMap=item.get("tasksMap", {}),
                #     )
        except Exception as e:
            print(f"Error with fetching calendar data: {e}")

    @classmethod
    def getWeek(cls, request) -> JsonResponse:
        if request.method == "GET":
            # this is just to test the data
            cls.__setUpWeek()
            print(cls.__week)
            return JsonResponse(cls.__week)

    # @classmethod
    # def __setToday(cls) -> None:

    @classmethod
    def getToday(cls, response) -> JsonResponse:
        if response.method == "GET":
            cls.__setUpTodayTasks()
            return JsonResponse(cls.__todayTasks)

    @classmethod
    def getCustomizedWeek(cls):
        pass

    @classmethod
    def getTodos(cls, request) -> dict:
        if request.method == "GET":
            user_id = str(request.user)
            
            userTodos = cls.__todos[user_id]


            # Create a list of dictionaries for each Todo object
            todos_dict_list = [
                todo.to_dict() for todo in userTodos.values()
            ]  # Use to_dict()

            return todos_dict_list

    def getGoals(cls, request) -> JsonResponse:
        if request.method == "GET":
            pass

    @classmethod
    @csrf_exempt
    def create(cls, request) -> JsonResponse:
        if request.method == "POST":
            data = request.data
            item_type = data.get("item_type")
            user_id = str(request.user)

            if item_type == "TODO":
                title = data.get("title")
                content = data.get("content")
                completed = data.get("completed")
                id=user_id
                if title in cls.__todos:
                    return JsonResponse(
                        {"error": "Todo item with this title already exists"},
                        status=400,
                    )

                cls.__todos[user_id][title] = Todo(
                    id=user_id, title=title, content=content, completed=completed
                )

                response = cls.__table.put_item(
                    Item={
                        "id#title": "#".join([id, title]),
                        "id#item_type": "#".join([id, item_type]),
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

                # remember to change to support 2d dict
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

            elif item_type == "TASK" and title in cls.__tasks:
                cls.__table.delete_item(Key={"title": title, "item_type": item_type})
                del cls.__tasks[title]
                cls.__resetWeek()
                return JsonResponse(
                    {"message": "Todo deleted successfully."}, status=204
                )

            elif item_type == "FREQUENT":
                cls.__table.delete_item(Key={"title": title, "item_type": item_type})
                print(f"title: {title} \t item_type: {item_type}")
                for day in cls.__frequentTasks.keys():
                    if title in cls.__frequentTasks[day]:
                        del cls.__frequentTasks[day][title]  # This does delete
                        break

                cls.__resetWeek()
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
                newStatus = newStatus.get("completed")
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
            
            if item_type == "FREQUENT":
                newStatus = json.loads(request.body)
                newStatus = newStatus.get("completed")
                response = cls.__table.update_item(
                    Key={"title": title, "item_type": item_type},
                    UpdateExpression="set completed = :c",
                    ExpressionAttributeValues={":c": newStatus},
                    ReturnValues="UPDATED_NEW",
                )

                for day in cls.__frequentTasks.keys():
                    if title in cls.__frequentTasks[day]:
                        cls.__frequentTasks[day][title].completed = not(cls.__frequentTasks[day][title].completed)
                        break
                return JsonResponse(
                    {
                        "message": "Todo status updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )