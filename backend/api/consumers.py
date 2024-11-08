# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os
from .services.ScheduleManager import ScheduleManager
from .models.Task_Model import Task
from openai import OpenAI
from .models.UserData_model import UserData

# Load OpenAI API key from environment variables
# openai.api_key = os.getenv("OPENAI_API_KEY")

"""
    OPENAI Reponses Structure
    {
        "role": "system",
        "content": (
            "You are a schedule manager. You will process user input and organize "
            "the data in JSON format based on the user's requests. A task can only have "
            "the following attributes: 'title', 'content', 'timeFrame' (formatted as HH:MM, HH:MM), "
            "'date' (formatted as MM-DD-YYYY), and 'item_type' set to 'TASK'. A Todo can only have "
            "the following attributes: 'title', 'content', 'date' (formatted as MM-DD-YYYY),  and 'item_type' set to 'TODO'. "
            "If user input involves generating/editing/deleting multiple tasks or todos, format the JSON response as a list. "
            "You will generate/delete/edit tasks or todos for the user. You will create a JSON list that contains "
            "'toCreate', 'toDelete', 'toEdit', and 'toUpdate'. If creating a task/todo, it will go under 'toCreate', "
            "if deleting a task/todo, it will go under 'toDelete', if editing a task/todo, it will go under 'toEdit', "
            "and if updating a task/todo, it will go under 'toUpdate'.
        )
        },
        {
        "role": "system",
        "content": (
            "Process only the current user request for creating, deleting, or editing tasks without referencing past tasks."
            "Consider today's date Wednesday 11/06/2024, and these rest of the week, Thursday 11/07/2024, Friday 11/08/2024, Saturday 11/09/2024,
            Sunday 11/11/2024, Monday 11/12/2024, Tuesday 11/13/2024.
        )
        },
        {
        "role": "system",
        "content": (
            "When the user requests to delete a task or todo, you will infer the necessary details based on the user's input. "
            "If the user mentions a task (e.g., 'doctor's appointment') but does not specify a date or time, you will assume: "
            "- The task's title based on the user's input (e.g., 'Doctor's appointment'). "
            "- The date will be set to the current date or the next day if the request is about a future task (e.g., 'tomorrow' means the next day's date). "
            "- The item type will be set to 'UNKNOWN' if not specified. "
            "You will then create an item in the 'toDelete' list with the inferred values and include the following attributes: "
            "- 'title': The inferred title of the task. "
            "- 'content': A brief description or repetition of the task's title. "
            "- 'date': The date on which the task is scheduled or intended to be deleted. "
            "- 'item_type': Set to 'UNKNOWN' if not specified. "
            "The response will contain a JSON list with the 'toCreate', 'toDelete', 'toEdit', and 'toUpdate' keys."
        )
        },
        {
        "role": "user",
        "content": "Hello! My name is Chris and you are my Assistant."
        }
"""


class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.user_id = str(self.scope["user"])
        self.user_data = ScheduleManager.get_user(self.user_id)
        # self.client = OpenAI()

        if self.user.is_authenticated:
            await self.accept()
            # Send an initial welcome message from the bot
            welcome_message = (
                f"Welcome to the chat {str(self.user)}! How can I assist you today?"
            )
            await self.send(text_data=json.dumps({"message": welcome_message}))
        else:
            # Reject the connection if the user is not authenticated
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        if not self.user.is_authenticated:
            await self.send(
                text_data=json.dumps(
                    {"message": "You must be logged in to use this feature."}
                )
            )
            return

        data = json.loads(text_data)
        user_message = data["message"]

        # Send the user message to OpenAI API
        messageToUser, toCreate, toDelete, toEdit = await self.get_bot_response(
            user_message
        )

        print("THSI IS TEH TODELETE")
        print(toDelete)

        # if the toCreate list is not empty

        if toDelete:
            self.delete_items(toDelete)
            
        if toCreate:
            self.create_items(toCreate)

            # first we need to check the task overlaps with another
        # if toEdit:
        #     self.edit_items(toEdit)

        # Send the bot response back to the WebSocket
        await self.send(text_data=json.dumps({"message": messageToUser}))

    async def get_bot_response(self, user_message):
        try:

            # This is where we are getting json from openAI api
            # Convert the JSON message to a dictionary
            botResponse = json.loads(user_message)

            # This message work with the json we get from openAI bot
            user_chat_message = botResponse.get("message", "Yeah I can do that.")
            to_create = botResponse.get("toCreate", [])
            to_delete = botResponse.get("toDelete", [])
            to_edit = botResponse.get("toEdit", [])

            self.formatTime(to_create)

            # Return response
            return user_chat_message, to_create, to_delete, to_edit

        except json.JSONDecodeError as e:
            return "Invalid JSON format."
        except Exception as e:
            return f"Error processing response: {str(e)}"

    async def get_delete_info(self, todos, tasks) -> list[str]:
        pass

    def create_items(self, toCreate) -> list[dict]:
        for item in toCreate:
            item_type = item["item_type"]
            # Handling tasks first:
            if item_type == "TODO":
                print("We will be creating this todo: ", item)
                ScheduleManager.create(
                    user_id=self.user_id,
                    item_type=item.get("item_type"),
                    content=item.get("content"),
                    completed=item.get("completed", False),
                    date=item.get("date"),
                    title=item.get("title"),
                )
            elif item_type == "TASK":
                task = Task(
                    item_id=None,
                    title=item.get("title"),
                    content=item.get("content"),
                    completed=item.get("completed", False),
                    timeFrame=item.get("timeFrame"),
                    date=item.get("date"),
                )
                overlapTasks = ScheduleManager.time_frame_overlap(
                    self.user_id, task, item["date"]
                )
                if overlapTasks is None:
                    # Handle if it does not overlap
                    ScheduleManager.create(
                        user_id=self.user_id,
                        item_type=item.get("item_type"),
                        content=item.get("content"),
                        completed=item.get("completed", False),
                        date=item.get("date"),
                        timeFrame=item.get("timeFrame"),
                        title=item.get("title"),
                    )
                else:
                    # This is how we will handle the task if it overlaps.
                    print("The task that it overlaps with is: ", overlapTasks)

    def delete_items(self, toDelete) -> list[dict]:
        # Getting all todos/tasks of the user
        todos, tasks = self.user_data.getAllData()

        # Getting the ids of the items to delete using the openAI api bot
        # idsToDelete = self.get_delete_info(todos, tasks)


        # Now deleting items based on id and item_type

        print("we are getting here")
        for item in toDelete:
            print("We are deleting this item", item['title'])


        # for item in toDelete:
        #     item_id = item["item_id"]
        #     item_type = item["item_type"]
        #     ScheduleManager.delete(self.user_id, item_id, item_type)

    def edit_items(self, toEdit) -> list[dict]:
        for item in toEdit:
            item_id = item["item_id"]
            item_type = item["item_type"]
            ScheduleManager.update(self.user_id, item_id, item_type)

    def formatTime(self, items):
        for item in items:
            if item["item_type"] == "TASK":
                item["timeFrame"] = self.convert_time_string(str(item["timeFrame"]))

    def convert_time_string(self, time_string):
        # Step 1: Remove the brackets
        time_string = time_string.strip("[]")

        # Step 2: Split by the comma
        time_list = time_string.split(",")

        # Step 3: Strip whitespace from each time
        time_list = [time.strip() for time in time_list]

        return time_list
