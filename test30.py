
import pathlib
import textwrap
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
GEMINI_API_KEY = genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# # Used to securely store your API key
# from google.colab import userdata

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def displayModels():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

model = genai.GenerativeModel('gemini-pro') #gemini-pro-vision


# generateContent = model.generate_content("What is your name?", safety_settings={'DANGEROUS_CONTENT':'block_none'}) # safety_settings={'DANGEROUS_CONTENT':'block_none'}
# print(generateContent.text)


def chatGemini1(input_text: str):
    chat = model.start_chat(history=[])
    try:
        response = chat.send_message(input_text, safety_settings={'HARASSMENT':'block_none'}, stream=True)
        #response.resolve()
    except Exception as e:
        print(f"Error occured while running Gemini: {e}")
        response = chat.send_message(input_text, safety_settings={'HARASSMENT':'block_none'})
    finally:
        response.resolve()
        print(response.text)
    
    while True:
        command = input("User: ")
        if "quit" == command:
            break
        chatGemini1(input_text=command)
        break
        
#chatGemini1(input_text="hi")

def chatGemini(messages, command):
    chat = model.start_chat(history=messages)
    try:
        response = chat.send_message(command, safety_settings={'HARASSMENT':'block_none'})
        print(response.text)
        
        messages.append(
            {
                'role':'model',
                'parts': response.text
            }
        )
        
        messages.append(
            {
                'role':'user',
                'parts': messages
            }
        )
        
    except Exception as e:
        print(f"Error occured while running Gemini: {e}")
        pass
    else:
        return response.text
    
    
if __name__ == '__main__':
    messages = [
        {
            'role':'user',
            'parts': ["Hi!"]
        }
    ]
    while True:
        command = input("User: ")
        if "quit" == command:
            break
        
        response = chatGemini(messages=messages, command=command)
        
        messages.append(
            {
                'role':'model',
                'parts': [response]
            }
        )
        
        messages.append(
            {
                'role':'user',
                'parts': [command]
            }
        )


#____________________________________________python test30.py
