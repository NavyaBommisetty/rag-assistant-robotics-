
from google.colab import drive
drive.mount('/content/drive')
print("✓ Google Drive mounted!")

!pip install -q langchain langchain-community faiss-cpu python-dotenv pypdf sentence-transformers ollama
print("✓ All libraries installed!")

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import LlamaCpp
import os
from pathlib import Path

print("✓ Libraries imported!")

print("✓ Using local FREE model (no API key needed)!")

pdf_folder_path = "/content/drive/MyDrive/rag_documents2"

print("Loading PDFs...")
pdf_files = list(Path(pdf_folder_path).glob("*.pdf"))
print(f"Found {len(pdf_files)} PDF files\n")

documents = []
for pdf_file in pdf_files:
    try:
        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()
        documents.extend(docs)
        print(f"  ✓ Loaded: {pdf_file.name} ({len(docs)} pages)")
    except Exception as e:
        print(f"  ✗ Error loading {pdf_file.name}: {e}")

print(f"\n✓ Total pages loaded: {len(documents)}")

print("✂️ Splitting documents into chunks...")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Size of each chunk
    chunk_overlap=200     # Overlap between chunks
)

chunks = splitter.split_documents(documents)
print(f"✓ Created {len(chunks)} chunks")

print("🔢 Creating FREE embeddings (using HuggingFace)...")
print("This may take 2-3 minutes (downloading model first time)...\n")

# FREE embedding model - no API key needed!
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("📦 Building vector store...")
vectorstore = FAISS.from_documents(chunks, embeddings)

print("✓ Vector store created!")

print("Creating RAG chain with FREE LLM...\n")

# Using a simpler approach - just use retriever to get context
# and format it nicely for the user

def simple_qa(question):
    """Simple QA without external LLM - uses retriever only"""
    docs = retriever.get_relevant_documents(question)
    return docs

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}  # Get top 5 relevant chunks
)

print("✓ RAG system ready (100% FREE, no API needed!)!")

def ask_question(question):
    print(f"\n❓ Question: {question}")
    print("-" * 70)
    
    try:
        # Get relevant documents
        docs = retriever.get_relevant_documents(question)
        
        # Format the answer from the documents
        if docs:
            print("Answer (from your documents):\n")
            answer_text = ""
            for i, doc in enumerate(docs[:3], 1):
                print(f"{i}. {doc.page_content[:500]}...")
                answer_text += doc.page_content + "\n"
            
            print("\n📌 Sources:")
            for i, doc in enumerate(docs[:3], 1):
                source_name = doc.metadata.get('source', 'Unknown')
                page_num = doc.metadata.get('page', 'N/A')
                print(f"  {i}. {source_name} (Page: {page_num})")
        else:
            print("No relevant documents found for your question.")
    except Exception as e:
        print(f"Error: {e}")
    
    print("-" * 70)


ask_question("What is the main topic of these documents?")

# Ask more questions
ask_question("Can you summarize the key points?")

ask_question("What are the important concepts discussed?")


print("\n Chat with your documents! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() == "quit":
        print("Goodbye! 👋")
        break
    
    if user_input:
        ask_question(user_input)
