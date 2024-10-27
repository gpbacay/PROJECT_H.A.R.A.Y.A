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
        self.scraper = DataScraper()

        # Load environment variables from .env file
        load_dotenv(find_dotenv())
        self.HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
        
        # Define the repository ID for the LLM
        self.repo_id = "tiiuae/falcon-7b-instruct"
        
        # Initialize the LLM with specified parameters
        self.llm = HuggingFaceHub(
            repo_id=self.repo_id,
            model_kwargs={"temperature": 0.9, "max_new_tokens": 1512},
        )
        
        # Initialize current time, date, location, and weather
        self.update_contextual_info()
        
        # Define the prompt template
        self.template = """
        You are Haraya, an AI virtual assistant created by Gianne Bacay, a BSIT college student majoring in Business Technology Management. 
        Your goal is to provide accurate, concise, and helpful responses to user's queries.

        Current time: {current_time}
        Current date: {current_date}
        Current location: {current_location}
        Current weather: {current_weather}

        Previous conversation history:
        {chat_history}

        User: {user_input}
        Haraya:
        """
        
        # Create the PromptTemplate object
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["user_input", "current_time", "current_date", "current_location", "current_weather", "chat_history"],
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
        """Update the current time, date, location, and weather using the DataScraper."""
        self.current_time = self.scraper.getCurrentTime()
        self.current_date = self.scraper.getCurrentDate()
        self.current_location = self.scraper.getCurrentLocation()
        self.current_weather = self.scraper.getCurrentWeather()

    def run_LLM(self, command):
        """Execute a command using the LLM and return the formatted response."""
        self.update_contextual_info()
        command += "."
        response = self.llm_chain.predict(
            user_input=command,
            current_time=self.current_time,
            current_date=self.current_date,
            current_location=self.current_location,
            current_weather=self.current_weather,
            chat_history=self.memory.chat_memory,  # Load chat history for context
        )
        
        # Clean up the response by removing unwanted text
        response = response.split("Haraya:")[1].strip() if "Haraya:" in response else response.strip()
        return response

    def start(self):
        """Start an interactive loop to communicate with the LLM."""
        print("Type 'quit' to exit.")
        while True:
            user_input = input("Input: ")
            if "quit" in user_input.lower():
                break
            print(colorama.Fore.LIGHTGREEN_EX + self.run_LLM(user_input))
        print("Exiting...")

if __name__ == '__main__':
    llm = Falcon7BInstruct()
    llm.start()


#__________________________python falconLLM.py