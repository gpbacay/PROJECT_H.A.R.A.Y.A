from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class HarayaAgent:
    def __init__(self):
        # Define the prompt template with placeholders for context and user question.
        self.template = """
Chat history/Previous conversation: {context}

User: {question}

Haraya:"""
        # Initialize the model and prompt.
        self.model = OllamaLLM(model="qwen2:0.5b")
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model
        
        # Initial context defines the agent's persona.
        self.context = ("Your name is Haraya, you are a personal Artificial Intelligence Operating System assistant. "
                        "Answer reasonably and concisely.")

if __name__ == "__main__":
    agent = HarayaAgent()
    while True:
        user_input = input("User: ")
        if user_input.lower() == "quit":
            break
        # Generate the assistant's response using the chain.
        result = agent.chain.invoke({"context": agent.context, "question": user_input})
        print("Haraya:", result)
        # Update the conversation context with the latest exchange.
        agent.context += f"\nUser: {user_input}\nHaraya: {result}"




#____________________python haraya_agent.py

