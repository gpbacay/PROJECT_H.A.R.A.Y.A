import os
import google.generativeai as palm
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
GOOGLEAI_API_KEY = palm.configure(api_key=os.environ['GOOGLEAI_API_KEY'])


""" 
response = palm.generate_text(prompt="The opposite of hot is")
print(response.result) #  'cold.'
response = palm.chat(messages=["Hello."])
print(response.last) #  'Hello! What can I help you with?'
response.reply("Can you tell me a joke?") """

""" #____Text-Generation
model = "models/text-bison-001"
prompt = "how to cook pizza?"

palm2_llm = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=0.99,
    max_output_tokens=512,
    candidate_count=1,
)
print(palm2_llm.result) """

#_______ChatBot
examples = [
    (),
    ()
]

prompt = """Your name is HARAYA, a Virtual Assistant AI created by Gianne Bacay."""

context = """" Speak like you are a Virtual Assistant AI"""

response = palm.chat(
    messages=prompt,
    temperature=0.99,
    context=context
    #examples=examples,
    
)

while True:
    try:
        command = input("Human: ")
        if "quit" in command:
            break
        response = response.reply(command)
        print(response.last)
    except:
        continue

#___________pip install google-generativeai
#___________python test5.py