# 🤖 Agent 1: Smart Q&A Prompt Agent

![Agent Series](https://img.shields.io/badge/Series-Agent_Building-a78bfa)
![Agent Number](https://img.shields.io/badge/Agent-1_of_7-success)
![Model](https://img.shields.io/badge/LLM-Gemini_2.0_Flash-blue)
![Framework](https://img.shields.io/badge/UI-Streamlit-FF4B4B)

> **The entry point to the Agent-Building Series** — from zero to a conversational AI system in under 100 lines of Python.

---

## 🎯 What is This?

This is **Agent 1 of 7** in a progressive AI agent-building curriculum. It demonstrates the foundation of every AI agent: an LLM backbone shaped by a **System Prompt** to behave as a specialized expert, with in-session memory to hold context across turns.

Think of it like this:
```
User Message → System Prompt + History → Gemini 2.0 → Response
```

---

## 🧠 System Logic: How it Works

### The 3-Layer Architecture
```
┌─────────────────────────────────────────┐
│              Streamlit UI (app.py)       │  ← Presentation Layer
│   Chat bubbles, input box, sidebar      │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│           SmartQAAgent (agent.py)        │  ← Intelligence Layer
│   - System Prompt (Persona Engineering) │
│   - Chat Session (Conversation Memory)  │
│   - Error Handling + Retry Logic        │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│        Google Gemini 2.0 Flash API       │  ← LLM Layer
│   - Processes all messages + history    │
│   - Generates contextual responses      │
└─────────────────────────────────────────┘
```

### Why Gemini 2.0 Flash?
- **Free tier**: 15 requests/minute, 1M tokens/day
- **Fast**: Sub-second response times
- **Multimodal**: Extends to images/files in future agents

### The Prompt Engineering Magic
The **System Prompt** is the most critical part of any agent. It defines:
- **Persona**: Senior Data Engineer + Career Coach
- **Domain Boundaries**: What topics it knows
- **Tone**: Mentor, not textbook
- **Behaviour Rules**: Always give a follow-up question

---

## 🛠️ Step-by-Step: How We Built This

### Step 1: Chose the LLM & Configured the Client
```python
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash", system_instruction=SYSTEM_PROMPT)
```

### Step 2: Designed the System Prompt
Defined the agent's expertise (Data Engineering, APIs, Career) and communication style. This shapes every response the LLM generates.

### Step 3: Created a Persistent Chat Session
```python
self.chat = self.model.start_chat(history=[])
# Gemini automatically tracks conversation history in this session
response = self.chat.send_message(user_message)
```

### Step 4: Built the Streamlit Chat UI
Used `st.session_state` to persist messages across Streamlit re-runs, and custom CSS for the dark glassmorphism design.

### Step 5: Added Safety & Security
- API key loaded from `.env` locally, `st.secrets` in production
- Fallback error message if key is missing
- Try/except wrapping all API calls

---

## ⚙️ Setup & Run

1. **Clone the repo**
2. **Install**: `pip install -r requirements.txt`
3. **Get a free Gemini API key** at [aistudio.google.com](https://aistudio.google.com)
4. **Configure**: Copy `.env.example` → `.env`, add your key:
   ```
   GEMINI_API_KEY=your_key_here
   ```
5. **Run**: `streamlit run app.py`

---

## 🗺️ What's Next in the Series?

| Agent | Upgrade |
|-------|---------|
| **Agent 2** | + Web Search Tool (agent can look things up!) |
| **Agent 3** | + Long-Term Memory (remembers across sessions) |
| **Agent 4** | + ReAct Loop (plan → act → observe → repeat) |

---

*Agent 1 of 7 | Meghana Mareedu | AI Agent-Building Series*
