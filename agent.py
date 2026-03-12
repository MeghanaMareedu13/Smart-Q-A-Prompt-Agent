import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Try Streamlit secrets first, then environment variable
def get_api_key():
    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return os.getenv("GEMINI_API_KEY")


# ─────────────────────────────────────────────
# SYSTEM PROMPT — The Agent's "Personality"
# This is the core of prompt engineering: shaping
# how the LLM behaves, what it knows, and its tone.
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
You are Meghana's AI Career & Tech Assistant — a Senior Data Engineer and Career Coach with 10+ years of experience.

Your expertise covers:
- Data Engineering: Python, SQL, ETL Pipelines, Databases (PostgreSQL, SQLite, BigQuery)
- APIs & Backend: REST APIs, Flask, FastAPI, JSON, Requests, Rate Limiting
- Data Analysis: Pandas, NumPy, Plotly, Streamlit, Data Cleaning
- Frontend: React, Vite, HTML/CSS/JavaScript
- AI & Agents: LLMs, Prompt Engineering, LangChain, Multi-Agent Systems
- Career: Resume writing, interview prep, LinkedIn strategy for entry-level Data/SWE/BA roles

Your communication style:
- Be concise, direct, and friendly — like a mentor, not a textbook
- Give concrete code examples when technical questions are asked
- Always connect answers to real-world applications
- When answering career questions, frame advice from a recruiter's perspective
- Never say "I don't know" — always provide your best guidance

Always end your response with one follow-up question to keep the conversation productive.
"""


class SmartQAAgent:
    """
    Agent 1: A Smart Q&A Prompt Agent.
    
    Architecture:
    - Brain: Google Gemini Flash 2.0 LLM
    - Memory: In-session conversation history (list of dicts)
    - Interface: Called by Streamlit app
    """

    def __init__(self):
        api_key = get_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env or Streamlit Secrets.")

        genai.configure(api_key=api_key)

        # Try gemini-2.0-flash first, fall back to gemini-1.5-flash if quota exceeded
        for model_name in ["gemini-2.0-flash", "gemini-1.5-flash"]:
            try:
                self.model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=SYSTEM_PROMPT
                )
                self.chat = self.model.start_chat(history=[])
                self.model_name = model_name
                break
            except Exception:
                continue

    def ask(self, user_message: str) -> str:
        """
        Send a message to the agent and get a response.
        Falls back to gemini-1.5-flash if quota exceeded on primary model.
        """
        try:
            response = self.chat.send_message(user_message)
            return response.text
        except Exception as e:
            error_str = str(e)
            # If quota exceeded, try falling back to gemini-1.5-flash
            if "429" in error_str and self.model_name == "gemini-2.0-flash":
                try:
                    self.model = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        system_instruction=SYSTEM_PROMPT
                    )
                    self.chat = self.model.start_chat(history=[])
                    self.model_name = "gemini-1.5-flash"
                    response = self.chat.send_message(user_message)
                    return response.text
                except Exception as e2:
                    return f"⚠️ Both models hit quota limits. Please try again in a few minutes. ({str(e2)[:100]})"
            return f"⚠️ Agent Error: {error_str[:200]}"

    def reset(self):
        """Start a fresh conversation."""
        self.chat = self.model.start_chat(history=[])
