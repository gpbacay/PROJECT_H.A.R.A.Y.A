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
            model_kwargs={"temperature": 0.5, "max_new_tokens": 512},  # Adjusted temperature for more controlled responses
        )
        
        # Initialize current time, date, location, and weather
        self.update_contextual_info()
        
        # Define the prompt template
        self.template = """
Instructions:
You are Haraya, an AI personal assistant software developed by Gianne Bacay, an AI Researcher. 
Engage in a friendly and natural conversation with the user command, be confident and honest. 
Respond only to the user's command in one concise sentence without any extraneous formatting or text in your responses.
Current time: {current_time}
Current date: {current_date}
Current location: {current_location}
Current weather: {current_weather}


User Command: {user_input}
Haraya:
"""
        
        # Create the PromptTemplate object
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["user_input", "current_time", "current_date", "current_location", "current_weather", "chat_history"],
        )
        
        # Initialize conversation memory with a buffer window of 3 for better context
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            input_key="user_input",
            k=3,
        )
        
        # Create the LLMChain object after initializing llm, prompt, and memory
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

    def clean_response(self, response):
        """Clean up the response to ensure relevance and clarity."""
        response = response.strip().split("Haraya:")[-1].strip()
        return response if response else "Could you please rephrase that?"

    def run_LLM(self, command):
        """Execute a command using the LLM and return the formatted response."""
        self.update_contextual_info()
        command += "."
        
        # Load chat history for context
        chat_history = self.memory.load_memory_variables({})["chat_history"]

        # Get the AI response with all required inputs
        response = self.llm_chain.predict(
            user_input=command,
            chat_history=chat_history,
            current_time=self.current_time,
            current_date=self.current_date,
            current_location=self.current_location,
            current_weather=self.current_weather
        )

        # Clean up the response
        response = self.clean_response(response)

        # Save the user input and AI response to memory
        self.memory.save_context({"user_input": command}, {"chat_history": response})

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