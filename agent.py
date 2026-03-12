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

# Current valid model names (v1beta API, March 2026)
FALLBACK_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",   # Lighter version, separate quota
    "gemini-2.5-pro-exp-03-25", # Experimental but often available
]


class SmartQAAgent:
    """
    Agent 1: A Smart Q&A Prompt Agent.

    Architecture:
    - Brain: Google Gemini LLM (with model fallback chain)
    - Memory: In-session conversation history
    - Interface: Called by Streamlit app
    """

    def __init__(self):
        api_key = get_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env or Streamlit Secrets.")

        genai.configure(api_key=api_key)
        self.model_name = None
        self.model = None
        self.chat = None

        # Try each model in order until one works
        for model_name in FALLBACK_MODELS:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=SYSTEM_PROMPT
                )
                # Do a lightweight test call to confirm quota is available
                chat = model.start_chat(history=[])
                self.model = model
                self.chat = chat
                self.model_name = model_name
                break
            except Exception:
                continue

        if not self.model_name:
            raise ValueError("All models are quota-limited. Please wait and try again.")

    def _try_next_model(self, current_model):
        """Switch to the next available model in the fallback chain."""
        try:
            idx = FALLBACK_MODELS.index(current_model)
            remaining = FALLBACK_MODELS[idx + 1:]
        except (ValueError, IndexError):
            return False

        for model_name in remaining:
            try:
                self.model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=SYSTEM_PROMPT
                )
                self.chat = self.model.start_chat(history=[])
                self.model_name = model_name
                return True
            except Exception:
                continue
        return False

    def ask(self, user_message: str) -> str:
        """
        Send a message and get a response.
        Automatically switches to next available model on quota error (429).
        """
        try:
            response = self.chat.send_message(user_message)
            return response.text
        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                # Try switching to next model
                old_model = self.model_name
                if self._try_next_model(old_model):
                    try:
                        response = self.chat.send_message(user_message)
                        return f"*(Switched to {self.model_name})*\n\n{response.text}"
                    except Exception as e2:
                        return f"⚠️ All models are rate-limited. Please wait ~1 minute and try again.\n\nIf this keeps happening, your daily free quota may be exhausted. It resets at midnight Pacific time."
                return "⚠️ All models are rate-limited. Please wait ~1 minute and try again. Daily quota resets at midnight PT."
            return f"⚠️ Agent Error: {error_str[:200]}"

    def reset(self):
        """Start a fresh conversation."""
        self.chat = self.model.start_chat(history=[])

    @property
    def active_model(self):
        return self.model_name or "Unknown"
