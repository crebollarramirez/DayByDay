# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os

# Load OpenAI API key from environment variables
# openai.api_key = os.getenv("OPENAI_API_KEY")

"""
    OPENAI Reponses Structure
    {
    "role": "system",
    "content": "You are a schedule manager. You will process user input 
    and organize the data in JSON format based on the user's requests. 
    A task can only have the following attributes: 'title', 'content', 
    'timeFrame' (formatted as HH:MM, HH:MM), 'date' 
    (formatted as MM-DD-YYYY), and 'item_type' set to 'TASK'. 
    A Todo can only have the following attributes: 'title', 
    'content', and 'item_type' set to 'TODO'. If user input 
    involves generating multiple tasks or todos, format the 
    JSON response as a list. You will generate tasks or todos for 
    the user. Consider the following tasks to avoid overlapping with 
    user-provided tasks: [{\"title\": \"Day 1 - Go to party\", \"content\":
        \"Party with Angel\", \"timeFrame\": \"[16:00, 16:30]\", \"date\": 
        \"10-21-2024\"}]"
    }
"""

class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        
        if user.is_authenticated:
            await self.accept()
            # Send an initial welcome message from the bot
            welcome_message = f"Welcome to the chat {str(user)}! How can I assist you today?"
            await self.send(text_data=json.dumps({
                'message': welcome_message
            }))
        else:
            # Reject the connection if the user is not authenticated
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        user = self.scope['user']
        
        if not user.is_authenticated:
            await self.send(text_data=json.dumps({
                'message': "You must be logged in to use this feature."
            }))
            return

        data = json.loads(text_data)
        user_message = data['message']

        # Send the user message to OpenAI API
        messageToUser, toCreate, toDelete, toEdit = await self.get_bot_response(user_message)

        # Additional logic for handling tasks
        # ...

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

