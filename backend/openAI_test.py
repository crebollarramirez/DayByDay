import os
import openai
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

assistant = client.beta.assistants.create(
    name = "Math Tutor", 
    instructions= "You are a personal math tutor. Write and run code to answer math questions.",
    model="gpt-3.5-turbo"
)

thread = client.beta.threads.create()

messages = client.beta.threads.messages.create(
    thread_id = thread.id,
    role= "user",
    content = "Solve this problem 3x + 11 = 14"
)

run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)

while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
else:
    print("run is completed")

messages = list(client.beta.threads.messages.list(
    thread_id = thread.id
))

for message in reversed(messages):
    print(message.role + ": " + message.content[0].text.value)