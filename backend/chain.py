# backend/chain.py
import os
import pickle
from typing import List, Optional

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Globals in module for simplicity
vectorstore: Optional[FAISS] = None
retriever = None
qa_chain: Optional[ConversationalRetrievalChain] = None
memory_store = {}  # maps chat_id -> ConversationBufferMemory

OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
EMBED_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
INDEX_PATH = os.environ.get("FAISS_INDEX_PATH", "faiss_index.pkl")

def init_llm_and_embeddings():
    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.0)
    emb = OpenAIEmbeddings(model=EMBED_MODEL)
    return llm, emb

def create_vectorstore_from_texts(texts: List[str], embeddings: OpenAIEmbeddings, persist: bool = True):
    """
    texts: list of raw text strings (documents)
    Splits -> embeds -> builds FAISS
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = []
    for t in texts:
        splits = text_splitter.split_text(t)
        docs.extend([Document(page_content=s) for s in splits])
    db = FAISS.from_documents(docs, embeddings)
    if persist:
        with open(INDEX_PATH, "wb") as f:
            pickle.dump(db, f)
    return db

def load_vectorstore_if_exists(embeddings: OpenAIEmbeddings):
    global vectorstore, retriever, qa_chain
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "rb") as f:
            vectorstore = pickle.load(f)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    else:
        vectorstore = None
        retriever = None

def build_chain():
    """
    Initialize llm/embeddings/vectorstore and create the ConversationalRetrievalChain.
    """
    global qa_chain, retriever, vectorstore
    llm, embeddings = init_llm_and_embeddings()
    load_vectorstore_if_exists(embeddings)
    if vectorstore is None:
        # no docs yet — create an empty FAISS to avoid crashes (optional)
        vectorstore = FAISS.from_documents([], embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, return_source_documents=True)
    return qa_chain

def ingest_texts_and_update_index(texts: List[str]):
    """
    Ingests raw texts (e.g., parsed PDF/text files) and updates the FAISS index (append new docs).
    For simplicity, we rebuild the index from current texts (you can extend to incremental).
    """
    global vectorstore, retriever, qa_chain
    llm, embeddings = init_llm_and_embeddings()
    db = create_vectorstore_from_texts(texts, embeddings, persist=True)
    vectorstore = db
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, return_source_documents=True)
    return True

def get_memory_for_chat(chat_id: str) -> ConversationBufferMemory:
    if chat_id not in memory_store:
        memory_store[chat_id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return memory_store[chat_id]



