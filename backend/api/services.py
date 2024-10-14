from django.http import JsonResponse
from rest_framework.response import Response
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Todo, FrequentTask, Task, Goal, UserData
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr
import uuid

# from django.contrib.auth.models import User

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

    __users: dict[str, UserData] = {}
    # Private Class Member Variables
    __table = settings.TABLE

    # key : id
    __goals = {}

    # this works well
    @classmethod
    def getData(cls) -> None:

        try:
            response = cls.__table.scan()
            items = response.get("Items", [])

            for item in items:
                # Getting the data from database DYNAMODB
                user_id, item_type = item.get("user#item_type").split("#")
                user_id = str(user_id)

                _, item_id = item.get("user#item_id").split("#")
                content = item.get("content")
                isCompleted = item.get("completed")

                if user_id not in cls.__users:
                    cls.__users[user_id] = UserData(user_id)

                # Now setting the data to the correct user and correct type of data
                if item_type == "TODO":
                    todo = Todo(item_id, content, isCompleted)
                    cls.__users[user_id].add_todo(todo)

                elif item_type == "FREQUENT":
                    title = item.get("title")
                    timeFrame = item.get("timeFrame")
                    frequency = item.get("frequency")
                    freqTask = FrequentTask(
                        item_id, title, content, frequency, isCompleted, timeFrame
                    )
                    cls.__users[user_id].add_frequentTask(freqTask)

                elif item_type == "TASK":
                    title = item.get("title")
                    timeFrame = item.get("timeFrame")
                    date = item.get("date")
                    task = Task(user_id, title, content, isCompleted, timeFrame, date)
                    cls.__users[user_id].add_task(task)

        except Exception as e:
            print(f"Error with fetching calendar data: {e}")

    @classmethod
    def getWeek(cls, request, date) -> dict:
        # This will set up the date and START_DAY IS A CONSTANT AND SHOULD NOT BE CHANGED
        # START_DAY = datetime.strptime(date, "%m-%d-%Y").date()
        if request.method == "GET":
            user_id = str(request.user)

            # if user_id not in cls.__frequentTasks:
            #     cls.__frequentTasks[user_id] = {
            #         "MONDAY": {},
            #         "TUESDAY": {},
            #         "WEDNESDAY": {},
            #         "THURSDAY": {},
            #         "FRIDAY": {},
            #         "SATURDAY": {},
            #         "SUNDAY": {},
            #         "EVERYDAY": {},
            #         "BIWEEKLY": {},
            #         "MONTHLY": {},
            #         "YEARLY": {},
            #     }
            # if user_id not in cls.__tasks:
            #     cls.__tasks[user_id] = {}

            # week = {}
            # for i in range(1, 7):
            #     dayName = str(
            #         (START_DAY + timedelta(days=i)).strftime("%A")
            #     )  # getting the name of the day of the week from the date
            #     fullDay = (
            #         dayName
            #         + ", "
            #         + str((START_DAY + timedelta(days=i)).strftime("%B %d"))
            #     )  # full Day name for the day
            #     d = str((START_DAY + timedelta(days=i)).strftime("%m-%d-%Y"))

            #     # adding day name in week
            #     if dayName not in week:
            #         week[fullDay] = {}

            #     # Adding all tasks for that day into the week
            #     for title, task in cls.__frequentTasks[user_id][
            #         dayName.upper()
            #     ].items():
            #         week[fullDay][title] = task.toDict()

            #     if len(cls.__frequentTasks[user_id]['EVERYDAY']) != 0:
            #         for title, task in cls.__frequentTasks[user_id]['EVERYDAY'].items():
            #             week[fullDay][title] = task.toDict()

            #     if d in cls.__tasks[user_id]:
            #         for title, task in cls.__tasks[user_id][d].items():
            #             week[fullDay][title] = task.toDict()
            # return week

        return cls.__users[user_id].getWeek(date=date)

    @classmethod
    def getToday(cls, request, date) -> dict:
        if request.method == "GET":
            user_id = str(request.user)

            return cls.__users[user_id].getToday(date)

        # date = datetime.strptime(date, "%m-%d-%Y").date()
        # dayName = date.strftime("%A").upper()
        # date = date.strftime("%m-%d-%Y")

        # print(date)

        # if request.method == "GET":
        #     today = {}

        #     user_id = str(request.user)
        #     for title, task in cls.__frequentTasks[user_id][dayName].items():
        #         today[title] = task.toDict()

        #     print(str(date))
        #     if str(date) in cls.__tasks[user_id]:
        #         for title, task in cls.__tasks[user_id][date].items():
        #             today[title] = task.toDict()

        #     if len(cls.__frequentTasks[user_id]["EVERYDAY"]) != 0:
        #         for title, task in cls.__frequentTasks[user_id]["EVERYDAY"].items():
        #             today[title] = task.toDict()

    @classmethod
    def getCustomizedWeek(cls):
        pass

    @classmethod
    def getTodos(cls, request) -> dict:
        if request.method == "GET":
            user_id = str(request.user)
            return cls.__users[user_id].getTodos()

    def getGoals(cls, request) -> JsonResponse:
        if request.method == "GET":
            pass

    @classmethod
    @csrf_exempt
    def create(cls, request) -> Response:
        user_id = str(request.user)
        print(user_id)

        if request.method == "POST":
            data = request.data

            # ALL ITEMS HAVE THESE ATTRIBUTES
            item_type = data.get("item_type")
            content = data.get("content")
            completed = data.get("completed")

            if item_type == "TODO":
                item_id = str(uuid.uuid4())
                cls.__users[user_id].add_todo(
                    Todo(item_id=item_id, content=content, completed=completed)
                )

                response = cls.__table.put_item(
                    Item={
                        "user#item_type": "#".join([user_id, item_type]),
                        "user#item_id": "#".join([user_id, item_id]),
                        "content": content,
                        "completed": completed,
                    }
                )
            # elif item_type == "FREQUENT":
            #     title = data.get("title")
            #     content = data.get("content")
            #     frequency = list(data.get("frequency"))
            #     completed = data.get("completed")
            #     timeFrame = data.get("timeFrame")

            #     for freq in frequency:
            #         if title in cls.__frequentTasks[user_id][freq]:
            #             return Response(
            #                 {"error": "Frequent Task with this title already exists"},
            #                 status=400,
            #             )

            #     # remember to change to support 2d dict

            #     for freq in frequency:
            #         cls.__frequentTasks[user_id][freq.upper()][title] =

            #         FrequentTask(
            #             title=title,
            #             content=content,
            #             frequency=freq,
            #             completed=completed,
            #             timeFrame=timeFrame,
            #         )

            #         response = cls.__table.put_item(
            #             Item={
            #                 "id#title": "#".join([user_id, title]),
            #                 "id#item_type": "#".join([user_id, item_type]),
            #                 "content": content,
            #                 "frequency": freq,
            #                 "completed": completed,
            #                 "timeFrame": timeFrame,
            #             }
            #         )

            elif item_type == "TASK":
                title = data.get("title")
                content = data.get("content")
                completed = data.get("completed")
                timeFrame = data.get("timeFrame")
                date = data.get("date")

                item_id = str(uuid.uuid4())

                task = Task(
                    item_id=item_id,
                    title=title,
                    content=content,
                    completed=completed,
                    timeFrame=timeFrame,
                    date=date,
                )

                if cls.__users[user_id].create(task):
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
                    Response({"message": "Task was not created"}, status=400)

            return Response({"message": "Task Created", "data": data}, status=201)

    @classmethod
    @csrf_exempt
    def delete(cls, request, item_id, item_type) -> Response:
        user_id = str(request.user)
        if request.method == "DELETE":
            if item_type == "TODO":
                cls.__users[user_id].delete_todo(item_id)

                print()

                response = cls.__table.delete_item(
                    Key={
                        "user#item_type": "#".join([user_id, item_type]),
                        "user#item_id": "#".join([user_id, item_id]),
                    }
                )

                print(response)

                return Response({"message": "Todo deleted successfully."}, status=204)

            elif item_type == "TASK":
                cls.__users[user_id].delete_task(item_id)

                print("#".join([user_id, item_type]))
                print("#".join([user_id, item_id]))
                cls.__table.delete_item(
                    Key={
                        "user#item_type": "#".join([user_id, item_type]),
                        "user#item_id": "#".join([user_id, item_id]),
                    }
                )

                return Response({"message": "Todo deleted successfully."}, status=204)

            elif item_type == "FREQUENT":
                cls.__table.delete_item(
                    Key={
                        "user#item_type": "#".join([user_id, item_type]),
                        "user#item_id": "#".join([user_id, item_id]),
                    }
                )

                cls.__resetWeek()
                return Response({"message": "Todo deleted successfully."}, status=204)

    @classmethod
    @csrf_exempt
    def update(cls, request, item_id, item_type) -> Response:
        user_id = str(request.user)
        if request.method == "PUT":
            data = json.loads(request.body)
            if item_type == "TODO":
                newData = data.get("newData")
                cls.__users[user_id].update_todo(item_id, newData)

                response = cls.__table.update_item(
                    Key={
                        "user#item_id": user_id + "#" + item_id,
                        "user#item_type": user_id + "#" + item_type,
                    },
                    UpdateExpression="set content = :c",
                    ExpressionAttributeValues={":c": newData},
                    ReturnValues="UPDATED_NEW",
                )

                return Response(
                    {
                        "message": "Todo updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )

    @classmethod
    @csrf_exempt
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

            elif item_type == "FREQUENT":
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
                        "message": "Todo status updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )

    