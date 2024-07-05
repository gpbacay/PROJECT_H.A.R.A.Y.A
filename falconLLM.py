import os
import colorama
from dotenv import load_dotenv, find_dotenv
from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferWindowMemory
from webDataScrapingSystem import DataScraper

class Falcon7BInstruct:
    def __init__(self):
        colorama.init(autoreset=True)
        self.Scraper = DataScraper()
        
        # Load environment variables from .env file
        load_dotenv(find_dotenv())
        self.HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
        
        # Define the repository ID for the LLM
        self.repo_id = "tiiuae/falcon-7b-instruct"
        
        # Initialize the LLM with specified parameters
        self.llm = HuggingFaceHub(
            repo_id=self.repo_id,
            model_kwargs={"temperature": 0.01, "max_new_tokens": 1512},
        )
        self.llm.client.api_url = 'https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct'
        
        # Initialize current time, date, location, and weather
        self.update_contextual_info()
        
        # Define the prompt template
        self.template = """
        context:
        Listen to the user first.
        You are an AI virtual assistant named Haraya that follows instructions very well.
        You identify yourself as HARAYA.
        You are not allowed to lie or provide false information.
        If the given question is incomplete, ask for more information.
        If the human asks you a question, answer it directly and concisely.
        Do not generate additional content beyond the question.

        Haraya is an advanced AI virtual assistant created by Gianne Bacay, a BSIT college student majoring in Business Technology Management. 
        Haraya leverages machine learning, deep learning, computer vision, and NLP to offer personalized, human-like user experiences. 
        The name "Haraya" symbolizes limitless possibilities, embodying its mission to help users achieve their dreams and heralding a user-centric AI era. 
        Gianne Bacay is committed to advancing technology, aiming to achieve Artificial General Intelligence and transform human-computer interactions through Haraya.

        Current time: {current_time}
        Current date: {current_date}
        Current location: {current_location}
        Current weather: {current_weather}

        Previous conversation history: 
        {chat_history}

        Current conversation:
        User: {user_input}
        AI: """
        
        # Create the PromptTemplate object
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["chat_history", "user_input", "current_time", "current_date", "current_location", "current_weather"],
        )
        
        # Initialize conversation memory with a buffer window of 1
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            input_key="user_input",
            k=1,
        )
        
        # Create the LLMChain object
        self.llm_chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory,
        )
    
    def update_contextual_info(self):
        self.current_time = self.Scraper.getCurrentTime()
        self.current_date = self.Scraper.getCurrentDate()
        self.current_location = self.Scraper.getCurrentLocation()
        self.current_weather = self.Scraper.getCurrentWeather()

    def run_LLM(self, command):
        self.update_contextual_info()
        command += "."
        response = self.llm_chain.predict(
            user_input=command,
            current_time=self.current_time,
            current_date=self.current_date,
            current_location=self.current_location,
            current_weather=self.current_weather,
        )
        
        # Remove unwanted continuation
        if "User" in response:
            response = response.split("User")[0].strip()
        if "_" in response:
            response = response.split("_")[0].strip()
        if '"' in response:
            response = response.strip('"')
        return response

    def start(self):
        while True:
            user_input = input("Input: ")
            if "quit" in user_input:
                break
            print(colorama.Fore.LIGHTGREEN_EX + self.run_LLM(user_input))
        exit()

if __name__ == '__main__':
    llm = Falcon7BInstruct()
    llm.start()


#__________________________python falconLLM.py