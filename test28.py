from bardapi import Bard
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
api_key=os.environ['BARD_API_KEY']
bard = Bard(token = api_key)

def runBard(text):
    result = bard.get_answer(text)
    print(result.get("content"))
    
runBard(input("Input: "))

#____________________python test28.py