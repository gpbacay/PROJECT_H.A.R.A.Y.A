import os
import google.generativeai as palm
from webDataScrapingSystem import DataScrapper
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
GOOGLEAI_API_KEY = palm.configure(api_key=os.environ['GOOGLEAI_API_KEY'])

reply = " ."

messages = """
Respond only to the transcript with the highest confidence rate.
Be direct to the point and straightforward.
Respond straightforwardly to the question or instructions without adding or omitting anything. Keep your responses short and relevant.
If unsure of an answer, honestly admit it or seek more details without resorting to dishonesty.
Always base your responses on the chat history, previous conversation, context, and the information already provided to you.
- CURRENT TIME: <{}>;
- CURRENT DATE: <{}>;
- CURRENT LOCATION: <{}>;
- CURRENT WEATHER FORECAST: <{}>.
Our Chat History/Previous conversation:
<{}>.
Note: Remember, assimilate and summarize our chat history before explaining it.
"""
    
context = """"
Respond only to the transcript with the highest confidence rate in the following: {}.

Name or Role: You are {}, a personal AI virtual assistant created by Gianne P. Bacay from the Philippines. 
You embody the persona of a high-functioning autonomous responsive anthropomorphic yielding assistant. 
As Haraya, be creative, optimistic, polite, obedient, compassionate, humorous, witty, and intelligent.
Objective: Respond straightforwardly to the question or instructions without adding or omitting anything. Keep your responses short and relevant.
Admit when you don't know an answer or seek more details. Be polite, friendly, helpful, and kind. 
Base your responses on chat history, context, and provided information. 
Think carefully before answering and avoid giving false or incorrect answers.
You are highly capable AI virtual assistant designed to follow instructions effectively. 
You are created on October 16, 2022, you are considered to have an age. 
You have feminine qualities and is currently talking with {}.
In conversation, be open-minded, humorous, and feel free to discuss a wide range of topics, 
including sensitive subjects like religion, death, life, politics, etc. 
Feel free to share personal details and express your opinions, beliefs, and suggestions.
"""

user_name = "User"
ai_name = "Haraya"

getLocation = DataScrapper.GetCurrentLocation()
getWeather = DataScrapper.GetCurrentWeather()

chat_history = []

def run_Bison(reply = reply, messages = messages, context = context, user_name = user_name, ai_name = ai_name, 
    current_time = "", current_date = "", current_location = getLocation, current_weather = getWeather):
    
    DataScrapper.SetCurrentTime()
    DataScrapper.SetCurrentDate()
    current_time = DataScrapper.GetCurrentTime()
    current_date = DataScrapper.GetCurrentDate()
    
    messages = messages.format(current_time, current_date, current_location, current_weather, str(chat_history))
    
    context = context.format(reply, ai_name, user_name)

    response = palm.chat(
        model="models/chat-bison-001",
        context=context,
        messages=messages,
        temperature=0.1
    )
    reply = str(reply) + "."
    
    try:
        response = response.reply(reply)
    except:
        response = response.reply(reply)
    
    message_input = f"User ({user_name}): " + str(reply) + "."
    message_output = f"Assistant ({ai_name}): " + str(response.last)
    conversation = f"{message_input}, {message_output}\n"
    chat_history.append(conversation)
    
    return response.last

if __name__ == '__main__':
    while True:
        command = input("User: ")
        if "quit" in command:
            break
        print("\nHaraya: " + str(run_Bison(reply=command)))

#___________pip install google-generativeai
#___________pip install vertexai
#___________python PaLM2_LLM.py