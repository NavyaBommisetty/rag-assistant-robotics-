# rag-assistant-robotics-
RAG-based AI assistant for robotics documentation using LangChain
# RAG Assistant for Robotics

A question-answering chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions about robotics documentation.

## Features
- Loads and processes PDF documents
- Uses HuggingFace embeddings (free)
- Retrieves relevant sections from documents
- 100% free, no API costs

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
# Load your documents and chat
python main.py
```

## How it Works
1. Documents are loaded and split into chunks
2. Embeddings are created using HuggingFace
3. FAISS vector store stores the embeddings
4. When you ask a question, relevant sections are retrieved
5. System displays the most relevant content

## Files Used
- ai_robotics_rp.pdf
- IFR_Artificial_Intelligence_in_Robotics_Position_Paper_V02.pdf
- robotics_rf3.pdf

## Results
Successfully built RAG system that:
- Loads 58 pages from 3 PDFs
- Creates 313 chunks
- Answers questions with source citations
