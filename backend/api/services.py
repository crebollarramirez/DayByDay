import boto3
from .models import *
from django.http import JsonResponse
import json
from django.conf import settings
from enum import Enum
from django.views.decorators.csrf import csrf_exempt
from .models import *


class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Item_Type(Enum):
    TODO = "TODO"
    FREQUENT = "FREQUENT"
    TASK = "TASK"
    GOAL = "GOAL"


class ScheduleManager:

    # Private Class Member Variables
    __table = None

    __todos = {}
    __frquencyTasks = {}
    __tasks = {}
    __goals = {}

    # For displaying today and the week
    __today = {}
    __week = {}

    def __get_dynamodb_resource():
        return boto3.resource(
            "dynamodb",
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    @classmethod
    def __set_table(cls):
        dynamodb = cls.__get_dynamodb_resource()
        cls.__table = dynamodb.Table(settings.AWS_DYNAMODB_TABLE_NAME)

    # this works well
    @classmethod
    def getData(cls):
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

                # elif item_type == "FREQUENT":
                #     cls.__frquencyTasks[item['title']] = FrequentTask(
                #         title = item['title'],
                #         content = item['content'],
                #         frequency= item['frequency'],
                #         completed=item.get('completed', False),
                #         timeFrame= item.get('timeFrame')
                #     )
        except Exception as e:
            print(f"Error with fetching data: {e}")

    @classmethod
    def setUpWeek(cls) -> dict:
        cls.week

    @classmethod
    def getToday(cls) -> dict:
        return cls.today

    @classmethod
    def getCustomizedWeek(cls):
        pass

    @classmethod
    def getTodos(cls, request):
        if request.method == "GET":
            # Create a list of dictionaries for each Todo object
            todos_dict_list = [
                todo.to_dict() for todo in cls.__todos.values()
            ]  # Use to_dict()
            return JsonResponse(
                todos_dict_list, safe=False
            )  # Return list of dicts as JSON response

    @classmethod
    @csrf_exempt
    def create(cls, request):
        if request.method == "POST":
            data = json.loads(request.body)
            item_type = data.get("item_type")
            title = data.get("title")
            content = data.get("content")
            completed = data.get("completed")

            if item_type == "TODO":
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
            return JsonResponse({"message": "Task created", "data": data}, status=201)

    @classmethod
    @csrf_exempt
    def delete(cls, request, title, item_type):
        if request.method == "DELETE":
            if item_type == "TODO" and title in cls.__todos:
                cls.__table.delete_item(Key={"title": title, "item_type": item_type})
                del cls.__todos[title]
                return JsonResponse(
                    {"message": "Todo deleted successfully."}, status=204
                )

    @classmethod
    @csrf_exempt
    def update(cls, request, title, item_type):
        if request.method == "PUT":
            if item_type == "TODO":
                data = json.loads(request.body)
                print(data)
                newData = data.get("newData")
                response = cls.__table.update_item(
                    Key={"title": title, "item_type": item_type},
                    UpdateExpression="set content = :c",
                    ExpressionAttributeValues={":c": newData},
                    ReturnValues= "UPDATED_NEW"
                )

                cls.__todos[title].content = newData
            return JsonResponse({'message': 'Todo updated successfully', 'updated': response['Attributes']}, status=200)
