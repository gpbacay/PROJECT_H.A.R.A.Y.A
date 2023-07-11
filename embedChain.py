import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

from embedchain import App as ECApp
bot = ECApp()

bot.add("youtube_video", "https://www.youtube.com/watch?v=sv3TXMSv6Lw")

def run_embedChain(command):
    bot.query(command)

prompt = "how to cook pizza?"
print(run_embedChain(prompt))


#__________________python embedChain.py
