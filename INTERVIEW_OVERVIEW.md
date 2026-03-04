# 🎙️ Agent 1: Smart Q&A Prompt Agent — Interview-Ready Overview

---

## 1. The 30-Second Elevator Pitch
> "I built the first agent in my **7-part AI Agent-Building Series** using Google's Gemini 2.0 API. This isn't just a chatbot — it's a deliberately-architected **Prompt-Engineered Agent** with a specialized persona, domain expertise, and in-session memory. It demonstrates my understanding of LLM fundamentals: system prompting, chat sessions, token management, and production deployment via Streamlit Cloud."

---

## 2. Technical Highlights
- **System Prompt Engineering**: Crafted a 200-word system instruction that shapes the LLM's persona, domain knowledge, tone, and output format — the most critical skill in AI development today.
- **Stateful Chat Session**: Used `model.start_chat()` to maintain conversation history automatically, enabling multi-turn contextual responses — not just one-shot Q&A.
- **Secure Credential Management**: Implemented a 3-tier credential fallback: `(1) passed token → (2) st.secrets → (3) .env` — production-safe everywhere.

---

## 3. Design Decisions

### Why Gemini over GPT?
- **Free tier generosity**: 1M tokens/day vs. OpenAI's credit-based model.
- **Simpler client**: `google-generativeai` is cleaner for beginners to understand.
- **Portfolio differentiation**: Most agent tutorials use OpenAI; Gemini shows versatility.

### Why Streamlit (not Flask + React)?
- Speed to value: Full chat UI in 1 file vs. days of frontend work.
- Focus: The agent logic is the story — not the UI framework.

---

## 4. Sample Interview Q&A

### Q: "What is a system prompt, and why is it important?"
> "A system prompt is an invisible instruction given to the LLM before any user message. It's the primary tool for **Persona Engineering** — shaping how the model behaves, what it knows, and how it communicates. A well-crafted system prompt is the difference between a generic chatbot and a specialized expert system."

### Q: "How does your agent remember previous messages?"
> "I use Gemini's `start_chat()` API, which maintains a rolling `history` list of all previous turns. Each new message is sent alongside the full history, so the model always has context. This is called **Windowed Memory** — no external database needed for short sessions."

### Q: "What's the next step to make this production-grade?"
> "Two things: First, **Persistent Memory** across sessions using a vector database like Pinecone or ChromaDB — so the agent remembers users between visits. Second, **Tool Use** — giving the agent the ability to call external APIs, which is what I build in Agent 2."

---

*Agent 1 of 7 | Meghana Mareedu | AI Agent-Building Series*
