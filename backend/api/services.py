import json
from .ScheduleManager import ScheduleManager
from .Todo_Model import Todo
from .Task_Model import Task


class AIBot:
    @classmethod
    def handleUserMessage(cls, request, userInput: str):
        # We will input this response to the bot

        # The bot will return a proper structed response that we can work with.
        response = userInput

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

        response = json.loads(response)

        

        generated = []
        print(f"response from bot: {response}")
        for task in response:
            if str(task['item_type']) == str('TASK'):
                generated.append(Task)

    @classmethod
    def createTasks(cls):
        pass

    @classmethod
    def createWeekTemplate(cls):
        pass

    @classmethod
    def createTodo(cls):
        pass
