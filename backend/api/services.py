import boto3
from .models import *
from django.http import JsonResponse
import json
from django.conf import settings
from enum import Enum
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime, timedelta
import bcrypt

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
                # elif item_type == "GOAL":
                #     cls.__frequencyTasks[item["title"]] = Goal(
                #         title=item["title"],
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
    def getTodos(cls, request) -> JsonResponse:
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


class UserManager:
    __table = None
    __users_login = {}

    @classmethod
    def __set_table(cls) -> None:
        cls.__table = boto3.resource(
            "dynamodb",
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url="http://localhost:8080",  # For local DynamoDB instance
        ).Table(settings.AWS_DYNAMODB_TABLE_NAME2)

    @classmethod
    def getData(cls):
        cls.__set_table()
        try: 
            response = cls.__table.scan()
            items = response.get("Items", [])
            for item in items:
                attribute_type = item.get('attribute_type')
                if attribute_type == 'login':
                    username = item.get('username')
                    password = item.get('password')
                    
                    cls.__users_login[username] = User(
                        username=username,
                        password=password,
                    )
                    
        except Exception as e:
            print(f"Error with fetching user data: {e}")
        

    @classmethod
    def hash_password(cls, password) -> bcrypt:
        return str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))

    @classmethod
    def verify_password(cls, password, hashed_password) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# This works well
    @classmethod
    def create_user(cls, username, password) -> bool:
        if username in cls.__users_login: 
            return False
        hashed_password = cls.hash_password(password)

        cls.__users_login[username] = User(username=username, password=hashed_password)
        cls.__table.put_item(Item=cls.__users_login[username].to_dict()
        )

        return True
        

    @classmethod
    def authenticate_user(cls, username, password) -> False:
        if username not in cls.__users_login:
            return None
        
        user = cls.__users_login[username]

        if cls.verify_password(password, cls.__users_login[username].password):
            return user
        
        return None

    def get_user(cls,username) -> User:
        if username in cls.__users_login:
            return cls.__users_login[username]
        
        return None