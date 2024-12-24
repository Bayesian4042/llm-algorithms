from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ticket_price = {"hyderabad": 1000, "bangalore": 2000, "chennai": 1500, "mumbai": 2500}

def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called with destination_city: {destination_city}")
    city = destination_city.lower()
    return ticket_price.get(city, 0)

price_function = {
    "name": "get_ticket_price",
    "description": "Get ticket price for a destination city",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "Destination city"
            }
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": price_function}]


def chat(message, history):
    messages = [{"role": "system", "content": "Welcome to the ticket booking system"}]

    for human, assitant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assitant})
    messages.append({"role": "user", "content": message})
    response = openai.chat.completions.create(mode="gpt-4o-mini", messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        messages = response.choices[0].message
        response, city = handle_tool_call(messages)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(mode="gpt-4o-mini", messages=messages)
    
    return response.choices[0].message.content

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get("destination_city")
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": f"The ticket price for {city} is {price}",
        "tool_call_id": message.tool_calls[0].id
    }

    return response, city

history = []

while True:
    message = input("You: ")
    response = chat(message, history)
    print(f"Assistant: {response}")
    history.append((message, response))

    if "bye" in message:
        break



