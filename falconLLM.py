import os
from dotenv import load_dotenv, find_dotenv
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain

def run_falcon(command):
    
    load_dotenv(find_dotenv())
    HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

    
    repo_id = "tiiuae/falcon-7b-instruct"
    falcon_llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0.1, "max_new_tokens": 500})

    
    template = """
    You are a helpful AI assistant and provide the answer for the question asked politely.
    
    {question}"""

    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=falcon_llm)
    
    question = command
    response = llm_chain.run(question)
    return response

if __name__ == '__main__':
    run_falcon()


#__________________________python lamentis.py