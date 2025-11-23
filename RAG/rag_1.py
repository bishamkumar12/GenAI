from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from os import getenv

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from dotenv import load_dotenv

load_dotenv()

# Data Source 
pdf_path = Path(__file__).parent / "nodejs.pdf"
loader = PyPDFLoader(file_path=pdf_path)

docs = loader.load()  ## make pages

## Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000, 
    chunk_overlap =  200
)

split_docs = text_splitter.split_documents(documents=docs)


## Embeddings 
embeddings = GoogleGenerativeAIEmbeddings(
    model="text-embedding-004",                # correct model (Gemini API)
    google_api_key=getenv("GOOGLE_API_KEY")  #   uses your .env key
)

# storing the embddings in vector data base
vector_store = QdrantVectorStore.from_documents(
    documents=[],
    url = "http://localhost:6333/",
    collection_name = "learning_langchain", 
    embedding = embeddings
)


vector_store.add_documents(documents=split_docs)

print("Injection Done")