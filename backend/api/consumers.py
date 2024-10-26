# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
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
        user_message = data['message']

        # Send the user message to OpenAI API
        response = await self.get_bot_response(user_message)
        print(user_message)
        # Send the bot response back to the WebSocket
        await self.send(text_data=json.dumps({
            'message': response
        }))

    async def get_bot_response(self, user_message):
        # try:
        #     completion = openai.Completion.create(
        #         model="text-davinci-003",  # or whichever model you prefer
        #         prompt=user_message,
        #         max_tokens=50
        #     )
        #     response = completion.choices[0].text.strip()
        #     return response
        # except Exception as e:
        #     return "Sorry, I'm having trouble responding right now."

    
        return "This is the bot response: you said " + user_message
