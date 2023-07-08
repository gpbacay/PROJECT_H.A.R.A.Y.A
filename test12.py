import os
import google.generativeai as palm
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
GOOGLEAI_API_KEY = palm.configure(api_key=os.environ['GOOGLEAI_API_KEY'])

reply = ""

messages = """
    Mimic the question/text_input/mathematical expression or equation do not answer it nor solve it.
    text_input = text_output or answer = question.
    Copy the examples and follow the context.
    Start mimicking the text_input: {}.
    Format: text_output: {}
    Also, while mimicking remember what you are mimicking.
    """
    
context = """"
    Act like a mimic. 
    Mimic the question/text_input/mathematical expression or equation do not answer it nor solve it.
    text_input = text_output or answer = question.
    Copy the examples and follow the context.
    Start mimicking the text_input: {}.
    Format: text_output: {}
    Also, while mimicking remember what you are mimicking.
    """
    
user_name = "Gianne P. Bacay"
ai_name = "HARAYA"
question = "who am I?"
examples = [
    ("hi", "hi"),
    ("who am I?", "who am I?"),
    ("what is your name?", "what is your name?")
]

def run_mimic(reply = reply, messages = messages, context = context):
    
    messages = messages.format(reply, reply, reply)
    
    context = context.format(reply, reply, reply)

    response = palm.chat(
        model="models/chat-bison-001",
        context=context,
        messages=messages,
        temperature=0.0,
        candidate_count=1,
        top_k=1,
        top_p=0.0
    )
    questions = []
    question = ""
    response = response.reply(reply)
    response = response.last
    
    questions.append(response)
    question = questions[-1]
    question = question.split("\n\n")
    question = question[-1]
    question = question.split(": ")
    question = question[-1]
    
    return question

if __name__ == '__main__':
    while True:
        command = "text_input: " + str(input())
        if "quit" in command:
            break
        print(run_mimic(reply=command))

#___________pip install google-generativeai
#___________pip install vertexai
#___________python test12.py