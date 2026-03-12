import streamlit as st
from agent import SmartQAAgent

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Smart Q&A Agent | Meghana AI",
    page_icon="🤖",
    layout="centered"
)

# ─── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0e0e0;
    }
    /* Chat bubbles */
    .user-msg {
        background: linear-gradient(90deg, #4776E6, #8E54E9);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        margin: 8px 0;
        max-width: 80%;
        float: right;
        clear: both;
        color: white;
        font-size: 0.95rem;
    }
    .agent-msg {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px 18px 18px 4px;
        padding: 12px 18px;
        margin: 8px 0;
        max-width: 85%;
        float: left;
        clear: both;
        color: #e0e0e0;
        font-size: 0.95rem;
    }
    .clearfix { clear: both; }
    /* Title styling */
    h1 { color: #a78bfa !important; }
    .subtitle { color: #94a3b8; font-size: 0.9rem; margin-top:-10px; }
    .badge {
        display: inline-block;
        background: rgba(167,139,250,0.15);
        border: 1px solid #a78bfa;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.8rem;
        color: #a78bfa;
        margin: 2px;
    }
    /* Reset button */
    .stButton button {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.15);
        color: #e0e0e0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────
st.title("🤖 Smart Q&A Agent")
st.markdown('<p class="subtitle">Agent 1 of 7 — Powered by Google Gemini 2.0</p>', unsafe_allow_html=True)

st.markdown("""
<span class="badge">🐍 Python</span>
<span class="badge">📊 Data Engineering</span>
<span class="badge">🔌 APIs</span>
<span class="badge">💼 Career Advice</span>
<span class="badge">⚛️ React & Frontend</span>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Ask me anything about Data Engineering, Python, SQL, APIs, or your career. I remember our conversation!")

# ─── Session State ──────────────────────────────────────────
if "agent" not in st.session_state:
    try:
        st.session_state.agent = SmartQAAgent()
        st.session_state.messages = []
    except ValueError as e:
        st.error(f"⚠️ {e}")
        st.info("👉 Get a free API key at [aistudio.google.com](https://aistudio.google.com) and add it as `GEMINI_API_KEY` in Streamlit Secrets or your `.env` file.")
        st.stop()

# ─── Render Chat History ───────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">👤 {msg["content"]}</div><div class="clearfix"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="agent-msg">🤖 {msg["content"]}</div><div class="clearfix"></div>', unsafe_allow_html=True)

# ─── Suggested Starter Questions ──────────────────────────
if not st.session_state.messages:
    st.markdown("#### 💡 Try asking:")
    starters = [
        "What's the difference between a Data Engineer and a Data Analyst?",
        "How do I handle API rate limits in Python?",
        "What should I put on my resume for entry-level Data Engineering?",
        "Explain ETL pipelines like I'm a beginner",
    ]
    cols = st.columns(2)
    for i, q in enumerate(starters):
        if cols[i % 2].button(q, key=f"starter_{i}"):
            # Inject as user input
            with st.spinner("Thinking..."):
                response = st.session_state.agent.ask(q)
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# ─── Chat Input ────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    user_input = col1.text_input("", placeholder="Ask me anything about tech or your career...", label_visibility="collapsed")
    submitted = col2.form_submit_button("Send ➤")

if submitted and user_input.strip():
    with st.spinner("🤖 Agent thinking..."):
        response = st.session_state.agent.ask(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ─── Sidebar: Controls & Info ──────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 Agent Info")
    model_display = st.session_state.agent.active_model if "agent" in st.session_state else "Loading..."
    st.markdown(f"""
| Property | Value |
|----------|-------|
| **Model** | {model_display} |
| **Type** | Prompt Agent |
| **Memory** | In-session |
| **Agent #** | 1 of 7 |
""")
    st.markdown("---")
    st.markdown("### 📖 How it works")
    st.markdown("""
1. Your message is sent to **Gemini 2.0**
2. The LLM uses the **System Prompt** to behave like a tech mentor
3. **Conversation history** is maintained so it remembers context
4. Response is streamed back to the UI
""")
    st.markdown("---")
    if st.button("🗑️ Reset Conversation"):
        st.session_state.agent.reset()
        st.session_state.messages = []
        st.rerun()

# ─── Footer ────────────────────────────────────────────────
st.markdown("---")
st.caption("Agent 1 | Smart Q&A Prompt Agent | Meghana Mareedu — 30-Day AI Challenge")
