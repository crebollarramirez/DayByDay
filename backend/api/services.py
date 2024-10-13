from .models import *
from django.http import JsonResponse
from rest_framework.response import Response
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
    __frequentTasks = {}

    # key : id
    __tasks = {}
    __goals = {}

    # modify this later so it returns a value depending if it was able to connect to the database
    @classmethod
    def __set_table(cls) -> None:
        cls.__table = settings.TABLE

    # this works well
    @classmethod
    def getData(cls) -> None:
        cls.__set_table()

        try:
            response = cls.__table.scan()
            items = response.get("Items", [])

            for item in items:
                id, item_type = item.get("id#item_type").split("#")
                id = str(id)
                _, title = item.get("id#title").split("#")

                if id not in cls.__todos:
                    cls.__todos[id] = {}

                if id not in cls.__frequentTasks:
                    cls.__frequentTasks[id] = {
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

                if id not in cls.__tasks:
                    cls.__tasks[id] = {}

                if id not in cls.__tasks:
                    cls.__tasks[id] = {}

                if item_type == "TODO":
                    cls.__todos[id][title] = Todo(
                        id=id,
                        title=title,
                        content=item["content"],
                        completed=item.get("completed", False),
                    )
                elif item_type == "FREQUENT":
                    cls.__frequentTasks[id][item["frequency"]][title] = FrequentTask(
                        title=title,
                        content=item["content"],
                        frequency=item["frequency"],
                        completed=item.get("completed", False),
                        timeFrame=item.get("timeFrame"),
                    )
                elif item_type == "TASK":
                    date = item["date"]

                    if date not in cls.__tasks[id]:
                        cls.__tasks[id][date] = {}

                    cls.__tasks[id][date][title] = Task(
                        title=title,
                        content=item["content"],
                        completed=item.get("completed", False),
                        timeFrame=item.get("timeFrame"),
                        date=item.get("date"),
                    )
        except Exception as e:
            print(f"Error with fetching calendar data: {e}")

    @classmethod
    def getWeek(cls, request, date) -> dict:
        # This will set up the date and START_DAY IS A CONSTANT AND SHOULD NOT BE CHANGED
        START_DAY = datetime.strptime(date, "%m-%d-%Y").date()
        if request.method == "GET":
            user_id = str(request.user)

            if user_id not in cls.__frequentTasks:
                cls.__frequentTasks[user_id] = {
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
            if user_id not in cls.__tasks:
                cls.__tasks[user_id] = {}

            week = {}
            for i in range(1, 7):
                dayName = str(
                    (START_DAY + timedelta(days=i)).strftime("%A")
                )  # getting the name of the day of the week from the date
                fullDay = (
                    dayName
                    + ", "
                    + str((START_DAY + timedelta(days=i)).strftime("%B %d"))
                )  # full Day name for the day
                d = str((START_DAY + timedelta(days=i)).strftime("%m-%d-%Y"))

                if dayName not in week:
                    week[fullDay] = {}

                for title, task in cls.__frequentTasks[user_id][
                    dayName.upper()
                ].items():
                    week[fullDay][title] = task.toDict()

                if d in cls.__tasks[user_id]:
                    for title, task in cls.__tasks[user_id][d].items():
                        week[fullDay][title] = task.toDict()
            return week

    @classmethod
    def getToday(cls, request, date) -> dict:
        date = datetime.strptime(date, "%m-%d-%Y").date()
        dayName = date.strftime("%A").upper()
        date = date.strftime("%m-%d-%Y")

        print(date)

        if request.method == "GET":
            today = {}

            user_id = str(request.user)
            for title, task in cls.__frequentTasks[user_id][dayName].items():
                today[title] = task.toDict()

            print(str(date))
            if str(date) in cls.__tasks[user_id]:
                for title, task in cls.__tasks[user_id][date].items():
                    today[title] = task.toDict()

            return today

    @classmethod
    def getCustomizedWeek(cls):
        pass

    @classmethod
    def getTodos(cls, request) -> dict:
        if request.method == "GET":
            user_id = str(request.user)

            if user_id not in cls.__todos:
                cls.__todos[user_id] = {}
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
    def create(cls, request) -> Response:
        user_id = str(request.user)
        print(user_id)

        if request.method == "POST":
            data = request.data
            item_type = data.get("item_type")

            if item_type == "TODO":
                title = data.get("title")
                content = data.get("content")
                completed = data.get("completed")
                if title in cls.__todos[user_id]:
                    return Response(
                        {"error": "Todo item with this title already exists"},
                        status=400,
                    )

                cls.__todos[user_id][title] = Todo(
                    id=user_id, title=title, content=content, completed=completed
                )

                response = cls.__table.put_item(
                    Item={
                        "id#title": "#".join([user_id, title]),
                        "id#item_type": "#".join([user_id, item_type]),
                        "content": content,
                        "completed": completed,
                    }
                )
            elif item_type == "FREQUENT":
                title = data.get("title")
                content = data.get("content")
                frequency = list(data.get("frequency"))
                completed = data.get("completed")
                timeFrame = data.get("timeFrame")

                for freq in frequency:
                    if title in cls.__frequentTasks[user_id][freq]:
                        return Response(
                            {"error": "Frequent Task with this title already exists"},
                            status=400,
                        )

                # remember to change to support 2d dict

                for freq in frequency:
                    cls.__frequentTasks[user_id][freq.upper()][title] = FrequentTask(
                        title=title,
                        content=content,
                        frequency=freq,
                        completed=completed,
                        timeFrame=timeFrame,
                    )

                    response = cls.__table.put_item(
                        Item={
                            "id#title": "#".join([user_id, title]),
                            "id#item_type": "#".join([user_id, item_type]),
                            "content": content,
                            "frequency": freq,
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

                if date in cls.__tasks[user_id] and title in cls.__tasks[user_id][date]:
                    return Response(
                        {"error": "Task already exists"},
                        status=400,
                    )

                if date not in cls.__tasks[user_id]:
                    cls.__tasks[user_id][date] = {}

                cls.__tasks[user_id][date][title] = Task(
                    title=title,
                    content=content,
                    completed=completed,
                    timeFrame=timeFrame,
                    date=date,
                )

                response = cls.__table.put_item(
                    Item={
                        "id#title": "#".join([user_id, title]),
                        "id#item_type": "#".join([user_id, item_type]),
                        "content": content,
                        "completed": completed,
                        "timeFrame": timeFrame,
                        "date": date,
                    }
                )

            return Response({"message": "Task Created", "data": data}, status=201)

    @classmethod
    @csrf_exempt
    def delete(cls, request, title, item_type) -> Response:
        user_id = str(request.user)

        if request.method == "DELETE":
            if item_type == "TODO" and title in cls.__todos[user_id]:
                cls.__table.delete_item(
                    Key={
                        "id#title": user_id + "#" + title,
                        "id#item_type": user_id + "#" + item_type,
                    }
                )
                del cls.__todos[user_id][title]
                return Response({"message": "Todo deleted successfully."}, status=204)

            elif item_type == "TASK":
                cls.__table.delete_item(
                    Key={
                        "id#title": user_id + "#" + title,
                        "id#item_type": user_id + "#" + item_type,
                    }
                )

                for dateDict in cls.__tasks[user_id].values():
                    if title in dateDict:
                        del dateDict[title]
                        break

                return Response({"message": "Todo deleted successfully."}, status=204)

            elif item_type == "FREQUENT":
                cls.__table.delete_item(
                    Key={
                        "id#title": user_id + "#" + title,
                        "id#item_type": user_id + "#" + item_type,
                    }
                )

                for frequent in cls.__frequentTasks[user_id].keys():
                    if title in cls.__frequentTasks[user_id][frequent]:
                        del cls.__frequentTasks[user_id][frequent][title]
                        break

                cls.__resetWeek()
                return Response({"message": "Todo deleted successfully."}, status=204)

    @classmethod
    @csrf_exempt
    def update(cls, request, title, item_type) -> Response:
        user_id = str(request.user)
        if request.method == "PUT":
            if item_type == "TODO":
                data = json.loads(request.body)
                newData = data.get("newData")
                response = cls.__table.update_item(
                    Key={
                        "id#title": user_id + "#" + title,
                        "id#item_type": user_id + "#" + item_type,
                    },
                    UpdateExpression="set content = :c",
                    ExpressionAttributeValues={":c": newData},
                    ReturnValues="UPDATED_NEW",
                )

                cls.__todos[user_id][title].content = newData
                return Response(
                    {
                        "message": "Todo updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )

    @classmethod
    @csrf_exempt
    def changeStatus(cls, request, title, item_type) -> Response:
        user_id = str(request.user)
        if request.method == "PUT":
            if item_type == "TODO":
                newStatus = json.loads(request.body).get("completed")
                response = cls.__table.update_item(
                    Key={
                        "id#title": user_id + "#" + title,
                        "id#item_type": user_id + "#" + item_type,
                    },
                    UpdateExpression="set completed = :c",
                    ExpressionAttributeValues={":c": newStatus},
                    ReturnValues="UPDATED_NEW",
                )

                cls.__todos[user_id][title].completed = bool(newStatus)
                return Response(
                    {
                        "message": "Todo status updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )

            elif item_type == "FREQUENT":
                newStatus = json.loads(request.body)
                newStatus = newStatus.get("completed")
                response = cls.__table.update_item(
                    Key={
                        "id#title": user_id + "#" + title,
                        "id#item_type": user_id + "#" + item_type,
                    },
                    UpdateExpression="set completed = :c",
                    ExpressionAttributeValues={":c": newStatus},
                    ReturnValues="UPDATED_NEW",
                )

                for frequent in cls.__frequentTasks[user_id].keys():
                    if title in cls.__frequentTasks[user_id][frequent]:
                        cls.__frequentTasks[user_id][frequent][title].completed = not (
                            cls.__frequentTasks[user_id][frequent][title].completed
                        )
                        break

                return Response(
                    {
                        "message": "Todo status updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )
            elif item_type == "TASK":
                newStatus = json.loads(request.body)
                newStatus = newStatus.get("completed")
                response = cls.__table.update_item(
                    Key={
                        "id#title": user_id + "#" + title,
                        "id#item_type": user_id + "#" + item_type,
                    },
                    UpdateExpression="set completed = :c",
                    ExpressionAttributeValues={":c": newStatus},
                    ReturnValues="UPDATED_NEW",
                )

                print("this is running")
                for day in cls.__tasks[user_id].keys():
                    if title in cls.__tasks[user_id][day]:
                        cls.__tasks[user_id][day][title].completed = not (
                            cls.__tasks[user_id][day][title].completed
                        )
                return Response(
                    {
                        "message": "Todo status updated successfully",
                        "updated": response["Attributes"],
                    },
                    status=204,
                )

    """
    Check if two tasks overlap based on their time frames.

    :param task1: First task (FrequentTask or Task)
    :param task2: Second task (FrequentTask or Task)
    :return: True if the time frames overlap, False otherwise
    """

    def time_frame_overlap(task1, task2) -> bool:

        start1, end1 = task1.timeFrame
        start2, end2 = task2.timeFrame

        # Convert military time to minutes since midnight for comparison
        def military_to_minutes(military_time):
            hours, minutes = map(int, military_time.split(":"))
            return hours * 60 + minutes

        start1_minutes = military_to_minutes(start1)
        end1_minutes = military_to_minutes(end1)
        start2_minutes = military_to_minutes(start2)
        end2_minutes = military_to_minutes(end2)

        # Check for overlap
        return not (end1_minutes <= start2_minutes or end2_minutes <= start1_minutes)
