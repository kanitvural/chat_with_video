import os

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


llm_gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Talking with llm


def ask_gemini(prompt):

    AI_response = llm_gemini.invoke(prompt)
    return AI_response.content


# RAG - Transcrypted video texts


def rag_with_video_transcrypt(transcrypted_docs, prompt):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0, length_function=len
    )

    splitted_documents = text_splitter.split_documents(transcrypted_docs)
    vector_store = Chroma.from_documents(splitted_documents, embeddings)
    retriever = vector_store.as_retriever()

    relevant_documents = retriever.get_relevant_documents(prompt)

    context_data = " ".join(doc.page_content for doc in relevant_documents)

    final_prompt = f"""
    I have a question: {prompt}.
    To answer this question, I have the following information: {context_data}.
    Only use the information I've provided here to answer this question.
    Do not go beyond this information under any circumstances.
    """

    AI_response = ask_gemini(final_prompt)

    return AI_response, relevant_documents
