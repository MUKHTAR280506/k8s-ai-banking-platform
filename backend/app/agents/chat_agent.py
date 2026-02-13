from app.rag.retriever import fetch_rules
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def chat_reply(message: str) -> str:
    rules = fetch_rules(message)

    prompt = f"""
You are a professional banking assistant.
Respond clearly and politely.

Rules:
{rules}

User message:
{message}
"""

    return llm.predict(prompt).strip()
