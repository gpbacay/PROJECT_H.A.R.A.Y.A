import os
from dotenv import load_dotenv, find_dotenv
from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate, LLMChain

from langchain.memory import ConversationBufferWindowMemory

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

repo_id = "tiiuae/falcon-7b-instruct"
falcon_llm = HuggingFaceHub(
    repo_id=repo_id,
    model_kwargs={"temperature": 0.1, "max_new_tokens": 512}
)

template = """
context:
-You are an AI virtual assistant that follows intructions very well.
-You Identify yourself as HARAYA.
-You are having a conversation with a human.
-You provide a helpful straightforward answer based on the chat history, context, and/or instruction given.

take note:
-If the given question is unfinished then DO NOT complete the question and just answer directly.
-If the human instructed you to do something then follow it and respond like a normal human.
-If you do not know the answer to a question then truthfully admit that you don't know the answer.
-Human: is the one you are conversing with.
-AI: is you.


previous conversation history: 
{chat_history}

current conversation:
Human: {user_input}
AI:"""

prompt = PromptTemplate(
    template=template,
    input_variables=["chat_history", "user_input"],
)

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    input_key="user_input",
    k=1,
)

llm_chain = LLMChain(
    llm=falcon_llm,
    prompt=prompt,
    memory=memory,
)
    
def run_falcon(command):
    command = command + "."
    response = llm_chain.predict(user_input=command)
    if "User" in response:
        response = response.replace("User", "") 
    return response

if __name__ == '__main__':
    while True:
        user_input = input("Human: ")
        if "quit" in user_input:
            break
        print(run_falcon(user_input))

#if __name__ == '__main__':
#    run_falcon()

#__________________________python test6.py