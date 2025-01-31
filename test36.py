from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate



template = """
Chat history/Previous conversation: {context}

User: {question}

Haraya:
"""


model = OllamaLLM(model="deepseek-r1:1.5b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# result = model.invoke("hello world")
# result = chain.invoke({"context": "Instructions: Your name is Haraya so act as Haraya, an AI assistant created by Gianne Bacay. Answer the question concisely.", "question": "what is your name?"})

def handle_conv():
    context="Your name is Haraya and I am the User. Answer directly and concisely."
    while True:
        user_input = input("User: ")
        if user_input.lower() == "quit":
            break
        result=chain.invoke({"context": context, "question": user_input})
        print("Haraya: ", result)
        context+=f"User: {user_input}\nHaraya: {result}"


if __name__ == "__main__":
    handle_conv()




# python test36.py





