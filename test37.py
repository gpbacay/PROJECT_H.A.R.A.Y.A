import threading
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class HarayaAgent:
    def __init__(self):
        # Define the prompt template with placeholders for context and user question.
        self.template = """
        Chat history/Previous conversation: {context}

        User: {question}

        Haraya:
        """
        # Initialize the model and prompt.
        self.model = OllamaLLM(model="qwen2:0.5b")
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model
        
        # Initial context defines the agent's persona.
        self.context = "Your name is Haraya, my personal AI assistant. Answer directly and concisely."
        self.running = True
        self.thread = None

    def run(self):
        """Runs the conversation loop in a separate thread."""
        while self.running:
            user_input = input("User: ")
            if user_input.lower() == "quit":
                self.running = False
                break
            # Generate the assistant's response using the chain.
            result = self.chain.invoke({"context": self.context, "question": user_input})
            print("Haraya:", result)
            # Update the conversation context with the latest exchange.
            self.context += f"\nUser: {user_input}\nHaraya: {result}"

    def start(self):
        """Starts the agent in a new thread."""
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        """Stops the agent and waits for the thread to finish."""
        self.running = False
        if self.thread is not None:
            self.thread.join()

if __name__ == "__main__":
    agent = HarayaAgent()
    agent.start()





#____________________python test37.py
# REMARKS: PERFECT MODEL




