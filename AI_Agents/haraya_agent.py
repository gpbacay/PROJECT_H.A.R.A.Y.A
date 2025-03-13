from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from web_data_scraping_system import DataScraper

class HarayaAgent:
    def __init__(self, ai_name: str = "Haraya", user_name: str = "User", model_id: str = "qwen2:0.5b") -> None:
        """
        Initializes the HarayaAgent with customizable parameters.
        
        :param ai_name: The name of the AI assistant.
        :param user_name: The name of the user.
        :param model_id: The identifier for the language model to use.
        """
        self.ai_name = ai_name
        self.user_name = user_name
        self.model_id = model_id
        
        # Initialize DataScraper for real-time data
        self.data_scraper = DataScraper()
        self.update_realtime_data()
        
        # Define the prompt template with placeholders for conversation context, and user question.
        self.template = f"""
Chat history/Previous conversation: {{context}}

{self.user_name}: {{question}}.

{self.ai_name}:"""
        
        # Initialize the language model and prompt.
        self.model = OllamaLLM(model=self.model_id)
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model
        
    def update_realtime_data(self):
        """Fetches the latest real-time data from DataScraper."""
        self.current_time = self.data_scraper.getCurrentTime()
        self.current_date = self.data_scraper.getCurrentDate()
        self.current_location = self.data_scraper.getCurrentLocation()
        self.current_weather = self.data_scraper.getCurrentWeather()
        
        self.context = (
            f"Your name is {self.ai_name}, an AI OS assistant made by Gianne Bacay.\n"
            f"Updated Real-time Info:\n"
            f"- Time: {self.current_time}\n"
            f"- Date: {self.current_date}\n"
            f"- Location: {self.current_location}\n"
            f"- Weather: {self.current_weather}\n"
            "Respond directly and concisely to the user's queries."
        )
    
    def get_response(self, question: str) -> str:
        """
        Generates the assistant's response for a given question.
        Fetches updated real-time data before responding.

        :param question: The user's question.
        :return: The assistant's response.
        """
        # Refresh real-time data before generating a response
        self.update_realtime_data()
        
        result = self.chain.invoke({
            "context": self.context,
            "question": question,
        })
        
        return result

if __name__ == "__main__":
    agent = HarayaAgent(ai_name="Haraya", user_name="Gianne", model_id="qwen2:0.5b")
    print("Haraya AI Initialized. Type 'quit' to exit.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "quit":
            print(f"{agent.ai_name}: Goodbye!")
            break
        result = agent.get_response(user_input)
        print(f"{agent.ai_name}: {result}")



#____________________python haraya_agent.py

