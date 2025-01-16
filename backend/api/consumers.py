# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os
from .services.ScheduleManager import ScheduleManager
from .models.Task_Model import Task
from openai import OpenAI
from .models.UserData_model import UserData
import openai
from django.conf import settings

# Load OpenAI API key from environment variables


class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        # Checking if the user is authenticated
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

        # User stuff
        self.user_id = str(self.scope["user"])
        self.username = str(self.scope["user"])
        self.user_data = ScheduleManager.get_user(self.user_id)

        # Assistant and thread initialization
        self.client = settings.OPENAI_CLIENT
        self.assistant = self.client.beta.assistants.retrieve(
            assistant_id=settings.ASSISTANT_ID
        )

        self.thread = self.client.beta.threads.create()

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
        # messageToUser, toCreate, toDelete, toEdit = await self.get_bot_response(
        #     user_message
        # )

        # response = await self.get_bot_response(user_message)
        # print(response)
        botResponse = await self.get_bot_response(user_message)

        # print("this is to delete")
        # print(toDelete)

        # # if the toCreate list is not empty

        # if toDelete:
        #     self.delete_items(toDelete)

        # if toCreate:
        #     await self.create_items(toCreate)

        # # if toEdit:
        # #     self.edit_items(toEdit)

        # # Send the bot response back to the WebSocket
        await self.send(text_data=json.dumps({"message": botResponse}))

    async def get_bot_response(self, user_message):
        try:

            # This is where we are getting json from openAI api
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id, role="user", content=user_message
            )

            # Now get the assistant's response (you may need to call a 'run' method depending on your setup)
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
            )

            while run.status != "completed":
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id, run_id=run.id
                )
            else:
                print("Run completed")

            messages = list(self.client.beta.threads.messages.list(thread_id=self.thread.id))

            for message in reversed(messages):
                print(message.role + ": " + message.content[0].text.value)

            # Get the most recent bot message
            reversedMessages = list(reversed(messages))
            most_recent_bot_message = reversedMessages[len(reversedMessages) - 1].content[0].text.value

            return most_recent_bot_message

            # Assuming the assistant responds with JSON, extract useful information
            # botResponse = response["choices"][0]["message"]["content"]

            # print(response)

            # await self.send(text_data=json.dumps({"message": str(response)}))

            # # This message work with the json we get from openAI bot
            # user_chat_message = botResponse.get("message", "Yeah I can do that.")
            # to_create = botResponse.get("toCreate", [])
            # to_delete = botResponse.get("toDelete", [])
            # to_edit = botResponse.get("toEdit", [])

            # self.formatTime(to_create)

            # Return response
            # return user_chat_message, to_create, to_delete, to_edit
            # return response

        except json.JSONDecodeError as e:
            await self.send(text_data=json.dumps({"message": "Invalid JSON format."}))
        except Exception as e:
            await self.send(
                text_data=json.dumps(
                    {"message": f"Error processing response: {str(e)}"}
                )
            )

    async def get_delete_info(self, todos, tasks) -> list[str]:
        pass

    async def create_items(self, toCreate) -> list[dict]:
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

                print("THIS THIS SHWOING THAT THE CREATE IS GETTING THERE")
                overlapTasks = ScheduleManager.time_frame_overlap(self.user_id, task)

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
                    await self.send(
                        text_data=json.dumps({"message": "There is an overlap!"})
                    )

                    print("THESE ARE THE OVERLAPPING TASKS")
                    print(overlapTasks)
                    # newTask:Task = await self.handleOverLappingTasks(task, overlapTasks)

                    # print("THIS IS THE NEW TASK", newTask.toDict())
                    # ScheduleManager.create(
                    #     user_id=self.user_id,
                    #     item_type="TASK",
                    #     content=newTask.content,
                    #     completed=newTask.completed,
                    #     date=newTask.date,
                    #     timeFrame=newTask.timeFrame,
                    #     title=newTask.title,
                    # )

    async def handleOverLappingTasks(
        self, task: Task, overlapTasks: list[Task]
    ) -> Task:
        return Task(
            title="new task",
            content="asdfasdfasdf",
            completed=False,
            timeFrame=["15:00", "16:00"],
            date="11-12-2024",
            item_id="af;lksjdlfafsdfjiiiiiii",
        )

    def delete_items(self, toDelete) -> list[dict]:
        # Getting all todos/tasks of the user
        todos, tasks = self.user_data.getAllData()

        # Getting the ids of the items to delete using the openAI api bot
        # idsToDelete = self.get_delete_info(todos, tasks)

        # Now deleting items based on id and item_type

        print("we are getting here")
        for item in toDelete:
            print("We are deleting this item", item["title"])

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
