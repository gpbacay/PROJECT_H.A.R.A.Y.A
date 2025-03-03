import os
import colorama
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

# Updated imports from langchain-community
from langchain_community.llms import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
)

# Updated imports from langchain-core and langchain
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from webDataScrapingSystem import DataScraper


class Falcon7BInstructRAG:
    def __init__(self):
        colorama.init(autoreset=True)
        self.scraper = DataScraper()
        
        print(colorama.Fore.LIGHTGREEN_EX + "Initializing RAG system...")
        
        # Load environment variables
        load_dotenv(find_dotenv())
        self.HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
        
        # Initialize the LLM
        self.repo_id = "tiiuae/falcon-7b-instruct"
        self.llm = HuggingFaceHub(
            repo_id=self.repo_id,
            model_kwargs={"temperature": 0.01, "max_new_tokens": 128},
            huggingfacehub_api_token=self.HUGGINGFACEHUB_API_TOKEN,
        )
        
        # Initialize embeddings model
        print(colorama.Fore.LIGHTGREEN_EX + "Loading embedding model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize vector store with documents
        print(colorama.Fore.LIGHTGREEN_EX + "Processing and embedding documents...")
        self.vector_store = self.initialize_knowledge_base()
        
        # Update contextual info (time, date, location, weather)
        self.update_contextual_info()
        
        # Define prompt template
        # The internal context is provided only for the model's use; it must not be output in the final response.
        self.template = """
System Instructions:
You are Haraya, an AI personal assistant. You have been given internal contextual information, which you must use to inform your answer but not repeat in your final output:
- Additional Context: {context}
- Current Time: {current_time}
- Current Date: {current_date}
- Current Location: {current_location}
- Current Weather: {current_weather}

When responding, answer directly and concisely to the user's command in one sentence without including any of the above context.

User: {user_input}
Haraya:"""
        
        # Create the PromptTemplate without exposing context in the final answer
        self.prompt = PromptTemplate(
            input_variables=["context", "user_input", "current_time", "current_date", 
                             "current_location", "current_weather"],
            template=self.template,
        )
        
        # Initialize conversation memory (hidden from the prompt template)
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            input_key="user_input",
            k=3,
            return_messages=True,
        )
        
        # Create LLM chain using the prompt and memory
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory,
            verbose=False
        )
        
        print(colorama.Fore.LIGHTGREEN_EX + "RAG system initialization complete!")

    def initialize_knowledge_base(self):
        """Initialize vector store with documents from multiple sources."""
        knowledge_base_dir = "knowledge_base"
        
        if not os.path.exists(knowledge_base_dir):
            os.makedirs(knowledge_base_dir)
            print(colorama.Fore.LIGHTGREEN_EX + f"Created knowledge base directory at {knowledge_base_dir}")
            return FAISS.from_texts(["Initial empty index"], self.embeddings)

        loaders = {
            "txt": (TextLoader, "**/*.txt"),
            "pdf": (PyPDFLoader, "**/*.pdf"),
            "csv": (CSVLoader, "**/*.csv"),
            "doc": (UnstructuredWordDocumentLoader, "**/*.doc*"),
            "ppt": (UnstructuredPowerPointLoader, "**/*.ppt*"),
        }

        documents = []
        
        for file_type, (loader_class, glob_pattern) in loaders.items():
            try:
                loader = DirectoryLoader(
                    knowledge_base_dir,
                    glob=glob_pattern,
                    loader_cls=loader_class
                )
                docs = loader.load()
                if docs:
                    print(colorama.Fore.LIGHTGREEN_EX + f"Loaded {len(docs)} {file_type} documents")
                    documents.extend(docs)
            except Exception as e:
                print(colorama.Fore.LIGHTRED_EX + f"Error loading {file_type} documents: {str(e)}")

        if not documents:
            print(colorama.Fore.LIGHTRED_EX + "No documents found in knowledge base directory")
            return FAISS.from_texts(["Initial empty index"], self.embeddings)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        splits = text_splitter.split_documents(documents)
        print(colorama.Fore.LIGHTGREEN_EX + f"Created {len(splits)} document chunks")

        vector_store = FAISS.from_documents(splits, self.embeddings)
        print(colorama.Fore.LIGHTGREEN_EX + f"Vector store created with {len(splits)} chunks")
        
        vector_store.save_local("faiss_index")
        return vector_store

    def update_contextual_info(self):
        """Update the current time, date, location, and weather."""
        try:
            self.current_time = self.scraper.getCurrentTime()
            self.current_date = self.scraper.getCurrentDate()
            self.current_location = self.scraper.getCurrentLocation()
            self.current_weather = self.scraper.getCurrentWeather()
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"Error updating contextual info: {str(e)}")
            now = datetime.now()
            self.current_time = now.strftime("%H:%M:%S")
            self.current_date = now.strftime("%Y-%m-%d")
            self.current_location = "Location unavailable"
            self.current_weather = "Weather data unavailable"

    def get_relevant_context(self, query):
        """Retrieve relevant context from the vector store."""
        try:
            docs = self.vector_store.similarity_search(query, k=3)
            return "\n".join(doc.page_content for doc in docs)
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"Error retrieving context: {str(e)}")
            return "No relevant context found."

    def run_LLM(self, command):
        """Execute a command using the RAG-enhanced LLM."""
        try:
            self.update_contextual_info()
            
            # Get relevant context
            context = self.get_relevant_context(command)
            
            # Prepare inputs for the prompt
            inputs = {
                "user_input": command,
                "context": context,
                "current_time": self.current_time,
                "current_date": self.current_date,
                "current_location": self.current_location,
                "current_weather": self.current_weather,
            }
            
            # Get response from the LLM chain
            response = self.chain.run(**inputs)
            
            return response.strip()
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"Error in run_LLM: {str(e)}")
            return "I encountered an error processing your request. Please try again."

    def start(self):
        """Start an interactive loop to communicate with the LLM."""
        print(colorama.Fore.LIGHTRED_EX + "Type 'quit' to exit.")
        while True:
            try:
                user_input = input("Input: ")
                if user_input.lower() == 'quit':
                    break
                print(colorama.Fore.LIGHTGREEN_EX + self.run_LLM(user_input))
            except KeyboardInterrupt:
                print(colorama.Fore.LIGHTRED_EX + "\nExiting...")
                break
            except Exception as e:
                print(colorama.Fore.LIGHTRED_EX + f"Error: {str(e)}")
        print(colorama.Fore.LIGHTRED_EX + "Exiting...")

if __name__ == '__main__':
    try:
        llm = Falcon7BInstructRAG()
        llm.start()
    except Exception as e:
        print(colorama.Fore.LIGHTRED_EX + f"Fatal error: {str(e)}")


#____________________python test34.py