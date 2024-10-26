# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import openai
import os

# Load OpenAI API key from environment variables
# openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data['message']

        # Send the user message to OpenAI API
        response = await self.get_bot_response(user_message)
        
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

    
        return "This is the bot response!"
