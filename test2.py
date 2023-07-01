import os
from dotenv import load_dotenv, find_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub


load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

repo_id = "tiiuae/falcon-7b-instruct"
falcon_llm = HuggingFaceHub(
    repo_id=repo_id,
    model_kwargs={"temperature": 0.1, "max_new_tokens": 512}
)

embeddings = HuggingFaceEmbeddings()
#loader = TextLoader("news/summary.txt")
loader = DirectoryLoader("news", glob="**/*.txt")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=2500, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

#Chroma vector store
vecstore = Chroma.from_documents(texts, embeddings)
qa = RetrievalQA.from_chain_type(
    llm=falcon_llm,
    chain_type="stuff",
    retriever=vecstore.as_retriever()
)

def query(q):
    print("Query: ", q)
    print("Answer: ", qa.run(q))
    
query("What are the effects of legislations surrounding emissions on the Australian coal market?")

#pip install sentence_transformers
#pip install transformers
#pip install InstructorEmbedding
#pip install chromadb
#__________________________python test2.py