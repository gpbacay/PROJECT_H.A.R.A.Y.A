#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import openai
from slowprint import slowprint 
import sys
import time
import os


class color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    UNDERLINE = '\033[4m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    YELLOW = '\033[93m'

openai.api_key = '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'


def gpt3_completion(prompt, engine='text-davinci-003', temp=0.7, top_p=1.0, tokens=600, freq_pen=0.0, pres_pen=0.0, stop=['<<END>>']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text

def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.1)

if __name__ == '__main__':
    os.system('clear')
    print()
    print(color.MAGENTA+"              ╔════════════════════════════════════╗"+color.END)
    print(color.MAGENTA+"              ║                                    ║ "+color.END)
    print(color.MAGENTA+"              ║       "+color.END+"Welcome to ChatGPT bot   "+color.MAGENTA+"    ║ "+color.END)
    print(color.MAGENTA+"              ║      "+color.END+"Developer:  Raffy Suarez   "+color.MAGENTA+"   ║ "+color.END)
    print(color.MAGENTA+"              ║                                    ║ "+color.END)
    print(color.MAGENTA+"              ╚════════════════════════════════════╝"+color.END)
    print()
    while True:
        prompt = input('What\'s on your mind?: '+color.CYAN)
        response = gpt3_completion(prompt)
        print_slow(color.END+f'\n\nBot Answer: \n{color.GREEN+response}\n\n\n'+color.END)
        
    