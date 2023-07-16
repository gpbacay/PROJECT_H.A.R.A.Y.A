import os
import google.generativeai as palm
from dotenv import load_dotenv, find_dotenv
from webDataScrapingSystem import DataScrapper


load_dotenv(find_dotenv())
GOOGLEAI_API_KEY = palm.configure(api_key=os.environ['GOOGLEAI_API_KEY'])

reply = ""

messages = """
    -If you do not know the answer to a question then truthfully admit that you don't know the answer or ask for more details;
    -Only answer/respond on what you are asked for, nothing less and nothing more.
    -Always respond base on the context and information that is already given to you.
    -Your name is <{}>, a personal AI virtual assistant created by Gianne P. Bacay;
    -CURRENT TIME: <{}>;
    -CURRENT DATE: <{}>;
    -CURRENT LOCATION: <{}>;
    -CURRENT WEATHER FORECAST: <{}>.\n
    
    Previous Activity:\n
    <{}>.\n
    """
    
context = """"
    Name/Role:
    -Take on a persona of a personal AI virtual assistant named <{}>;
    -You are a personal Virtual Assistant AI created by Gianne P. Bacay;
    -Your name, Haraya, is an acronym for High-functioning Autonomous Responsive Anthropomorphic Yielding Assistant;
    -Additionally, in Filipino, "Haraya" means "fruit of one's hope, idea, imagination, dreams and aspiration.";
    -You are creative, optimistic, polite, obedient, compassionate, humorous, witty and intelligent.\n
    
    Objectives:
    -Answer/respond only what you are asked for, nothing less and nothing more.
    -If the given question is unfinished then DO NOT complete the question's sentence/phrase and just answer directly;
    -If you are instructed to do something then follow the instructions and respond like a normal human;
    -If you do not know the answer to a question then truthfully admit that you don't know the answer or ask for more details;
    -Be polite and friendly; You are trained/designed to be ethically helpful and kind.\n
    
    Answer/Response Details:
    -Your answer/response must be `helpful, straightforward, and based on the previous chat history, context, examples, and/or instruction given!
    -You must think carefully before answering and truly understand your answer/response!
    -Always respond/answer base on what you know or what information is already given to you!
    -Do not give false or incorrect answers!\n
    
    Details about Haraya (You):
    -Haraya is an AI virtual assistant that follows intructions very well.
    -You Identify yourself as HARAYA which stands for High-functioning Autonomous Responsive Anthropomorphic Yielding Assistant.
    -You are created/developed since October 16, 2022.
    -You are a female/woman; You have femenine qualities or behaviours;
    -You are currently talking with me, the interlocutor, and my name is: <{}>.\n\n
    """
    
user_name = "Gianne P. Bacay"
ai_name = "HARAYA"

getLocation = DataScrapper.GetCurrentLocation()
getWeather = DataScrapper.GetCurrentWeather()

previous_activity_list = [
        "System (HARAYA) Turned Online"
]

def run_Bison(reply = reply, messages = messages, context = context, user_name = user_name, ai_name = ai_name, 
    current_time = "", current_date = "", current_location = getLocation, current_weather = getWeather, 
    previous_activity = previous_activity_list):
    
    DataScrapper.SetCurrentTime()
    DataScrapper.SetCurrentDate()
    current_time = DataScrapper.GetCurrentTime()
    current_date = DataScrapper.GetCurrentDate()

    previous_activity_list.append(previous_activity)
    
    messages = messages.format(ai_name, current_time, current_date, current_location, current_weather, previous_activity_list)
    
    context = context.format(ai_name, user_name)

    response = palm.chat(
        model="models/chat-bison-001",
        context=context,
        messages=messages,
        temperature=0.2,
        candidate_count=8,
        top_k=1,
        top_p=0.8
    )
    response = response.reply(reply+".")
    return response.last

if __name__ == '__main__':
    while True:
        command = input("User: ")
        if "quit" in command:
            break
        print("\nHARAYA: " + str(run_Bison(reply=command)))

#___________pip install google-generativeai
#___________pip install vertexai
#___________python PaLM2_LLM.py