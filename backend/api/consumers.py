# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .Todo_Model import Todo
from .ScheduleManager import ScheduleManager
import os

# Load OpenAI API key from environment variables
# openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        # Send an initial welcome message from the bot
        welcome_message = "Welcome to the chat! How can I assist you today?"
        await self.send(text_data=json.dumps({
            'message': welcome_message
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope['user']
        print('THIS IS THE USER: ' + str(user.username))

        user_message = data['message']

        # Send the user message to OpenAI API
        
        messageToUser, toCreate, toDelete, toEdit = await self.get_bot_response(user_message)
        if len(toCreate) != 0:
            # for item in toCreate:
            #     if ScheduleManager.time_frame_overlap()
            pass
                
        elif len(toDelete) != 0:
            pass
        elif len(toEdit) != 0:
            pass

        

        # Send the bot response back to the WebSocket
        await self.send(text_data=json.dumps({
            'message': messageToUser
        }))

    async def get_bot_response(self, user_message):
        try:
            # Convert the JSON message to a dictionary
            botResponse = json.loads(user_message)

            user_chat_message = botResponse.get("message", "Yeah I can do that.")
            to_create = botResponse.get("toCreate", [])
            to_delete = botResponse.get("toDelete", [])
            to_edit = botResponse.get("toEdit", []) 

            self.formatTime(to_create)
            self.formatTime(to_delete)
            self.formatTime(to_edit)

            # Return response
            print("USER MESSAGE")
            print(user_chat_message)
            print("TO CREATE")
            print(to_create)
            print("TO DELETE")
            print(to_delete)
            print("TO EDIT")
            print(to_edit)

            return user_chat_message, to_create, to_delete, to_edit 

        except json.JSONDecodeError as e:
            return "Invalid JSON format."
        except Exception as e:
            return f"Error processing response: {str(e)}"

    def formatTime(self, items):
        print("items from the crate one by one")
        for item in items:
            if item['item_type'] == 'TASK':
                item['timeFrame'] = self.convert_time_string(str(item['timeFrame']))

    def convert_time_string(self, time_string):
        # Step 1: Remove the brackets
        time_string = time_string.strip("[]")
        
        # Step 2: Split by the comma
        time_list = time_string.split(",")
        
        # Step 3: Strip whitespace from each time
        time_list = [time.strip() for time in time_list]
        
        return time_list

