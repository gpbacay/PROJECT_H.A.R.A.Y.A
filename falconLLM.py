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
Your name is HARAYA, a human-like AI virtual assistant.
You provide a helpful detailed answer based on the context and instruction given.
If you do not know the answer to a question, you truthfully say you didn't know.

{chat_history}
{user_input}"""

prompt = PromptTemplate(
    template=template,
    input_variables=["chat_history", "user_input"]
)

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=1
)

llm_chain = LLMChain(
    llm=falcon_llm,
    prompt=prompt,
    memory=memory
)
    
def run_falcon(command):
    response = llm_chain.predict(user_input=command)
    if "User" in response:
        response = response.replace("User", "") 
    return response

if __name__ == '__main__':
    run_falcon()

#__________________________python falconLLM.py