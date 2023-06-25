import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

from embedchain import App 
bot = App()

def run_embedChain(command):
    bot.query(command)

prompt = "how to cook pizza?"
run_embedChain(prompt)

#__________________python embedChain.py
