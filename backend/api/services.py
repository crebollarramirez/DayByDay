from rest_framework.response import Response
import json
from django.conf import settings
from .models import Todo, FrequentTask, Task, Goal, UserData
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
                    endFrequency = item.get("endFrequency")
                    freqTask = FrequentTask(
                        item_id, title, content, frequency, isCompleted, timeFrame, endFrequency
                    )
                    cls.__users[user_id].add_frequentTask(freqTask)

                elif item_type == "TASK":
                    title = item.get("title")
                    timeFrame = item.get("timeFrame")
                    date = item.get("date")
                    task = Task(user_id, title, content, isCompleted, timeFrame, date)
                    cls.__users[user_id].add_task_from_db(task)

        except Exception as e:
            print(f"Error with fetching calendar data: {e}")

    @classmethod
    def getWeek(cls, request, date) -> dict:
        if request.method == "GET":
            user_id = str(request.user)

            if user_id not in cls.__users:
                cls.__users[user_id] = UserData(user_id)
                
        return cls.__users[user_id].getWeek(date=date)

    @classmethod
    def getToday(cls, request, date) -> dict:
        if request.method == "GET":
            user_id = str(request.user)

            if user_id not in cls.__users:
                cls.__users[user_id] = UserData(user_id)

            return cls.__users[user_id].getToday(date)


    @classmethod
    def getCustomizedWeek(cls):
        pass

    @classmethod
    def getTodos(cls, request) -> dict:
        if request.method == "GET":
            user_id = str(request.user)

            if user_id not in cls.__users:
                cls.__users[user_id] = UserData(user_id)

            return cls.__users[user_id].getTodos()

    def getGoals(cls, request) -> None:
        if request.method == "GET":
            pass

    @classmethod
    def create(cls, request) -> Response:
        user_id = str(request.user)
        print(user_id)

        data = request.data

        # ALL ITEMS HAVE THESE ATTRIBUTES
        item_type = data.get("item_type")
        content = data.get("content")
        completed = data.get("completed")
        item_id = str(uuid.uuid4())

        if item_type == "TODO":
            cls.__users[user_id].add_todo(
                Todo(item_id=item_id, content=content, completed=completed)
            )

            cls.__table.put_item(
                Item={
                    "user#item_type": "#".join([user_id, item_type]),
                    "user#item_id": "#".join([user_id, item_id]),
                    "content": content,
                    "completed": completed,
                }
            )
        elif item_type == "TASK":
            title = data.get("title")
            content = data.get("content")
            completed = data.get("completed")
            timeFrame = data.get("timeFrame")
            date = data.get("date")

            task = Task(
                item_id=item_id,
                title=title,
                content=content,
                completed=completed,
                timeFrame=timeFrame,
                date=date,
            )

            if cls.__users[user_id].create_task(task):
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

        elif item_type == "FREQUENT":
            title = data.get("title")
            content = data.get("content")
            frequency = list(data.get("frequency"))
            completed = data.get("completed")
            timeFrame = data.get("timeFrame")
            endFrequency = data.get("endFrequency")


            freqTask = FrequentTask(item_id, title, content, frequency, completed, timeFrame, endFrequency)
            
            if cls.__users[user_id].add_frequentTask(freqTask):
                response = cls.__table.put_item(
                    Item={
                        "user#item_type": "#".join([user_id, item_type]),
                        "user#item_id": "#".join([user_id, item_id]),
                        "content": content,
                        "completed": completed,
                        "timeFrame": timeFrame,
                        "title": title,
                        "endFrequency": endFrequency,
                        "frequency": frequency
                    }
                )
            else:
                Response({"message": "Task was not created"}, status=400)

        return Response({"message": "Task Created", "data": data}, status=201)

    @classmethod
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
            if item_type == "TODO":
                cls.__users[user_id].update_todo(item_id, content)

                response = cls.__table.update_item(
                    Key={
                        "user#item_id": user_id + "#" + item_id,
                        "user#item_type": user_id + "#" + item_type,
                    },
                    UpdateExpression="set content = :c",
                    ExpressionAttributeValues={":c": content},
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
                date = data.get("date")

                cls.__users[user_id].update_task(item_id, title=title, content=content, timeFrame=timeFrame,date=date)
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

                cls.__users[user_id].update_frequentTask(item_id)



                
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