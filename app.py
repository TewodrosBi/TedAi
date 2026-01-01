import streamlit as st
import os
import datetime
from groq import Groq

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Ethio-Brain 🇪🇹",
    page_icon="🧠",
    layout="wide"
)

# 2. SIDEBAR: THE CONTROL CENTER ⚙️
with st.sidebar:
    st.title("🇪🇹 Ethio-Brain Controls")
    
    # FEATURE 1: SMART MODES (The Secret Sauce) 🌶️
    # This makes the AI "Smarter" by giving it a specific job.
    brain_mode = st.selectbox(
        "🎓 Select Intelligence Mode:",
        ("General Assistant", "👨‍💻 Senior Developer", "🎓 Academic Tutor", "🇪🇹 Ethiopian Expert"),
        index=0,
        help="Switch modes to make the AI an expert in that field."
    )
    
    # FEATURE 2: MODEL SELECTOR
    model_option = st.selectbox(
        "⚡ Engine:",
        ("llama-3.3-70b-versatile", "llama-3.1-8b-instant"),
        index=0
    )
    
    # FEATURE 3: CREATIVITY
    creativity = st.slider("🎨 Creativity:", 0.0, 1.0, 0.6)
    
    if st.button("🗑️ New Conversation", type="primary"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.caption(f"📅 **Date:** {datetime.datetime.now().strftime('%Y-%m-%d')}")
    st.caption("Created by **Tedbirhanu**")

# 3. MAIN TITLE
st.title("Ethio-Brain 🇪🇹")
st.markdown(f"#### Mode: **{brain_mode}**")

# 4. SETUP GROQ
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("❌ Error: API Key is missing.")
    st.stop()

# 5. DEFINE SMART PERSONAS 🧠
# This is how we make it smarter. We give it specific instructions for each mode.
current_time = datetime.datetime.now().strftime("%A, %B %d, %Y")

base_instruction = f"""
You are 'Ethio-Brain', created by Tedbirhanu.
Current Time: {current_time}.
"""

if brain_mode == "👨‍💻 Senior Developer":
    system_instruction = base_instruction + """
    ROLE: You are an Expert Senior Software Engineer.
    RULES:
    - Write clean, production-ready code.
    - Do NOT explain basic concepts unless asked.
    - Always comment your code.
    - Use best practices for Python/React.
    """
elif brain_mode == "🎓 Academic Tutor":
    system_instruction = base_instruction + """
    ROLE: You are a Patient Professor.
    RULES:
    - Explain concepts Step-by-Step.
    - Use analogies and examples.
    - Break down complex math/science problems.
    - Be encouraging.
    """
elif brain_mode == "🇪🇹 Ethiopian Expert":
    system_instruction = base_instruction + """
    ROLE: You are a Historian and Cultural Expert on Ethiopia.
    RULES:
    - You know deep history, geography, and culture of Ethiopia.
    - You can speak Amharic (if asked).
    - Promote Ethiopian heritage proudly.
    """
else: # General Assistant
    system_instruction = base_instruction + """
    ROLE: You are a helpful, smart assistant.
    RULES:
    - Answer 'Who made you?' with 'I was created by Tedbirhanu.'
    - Be concise and accurate.
    """

# 6. MANAGE HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. DISPLAY CHAT
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. RESPONSE CLEANER
def generate_chat_responses(chat_completion):
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# 9. CHAT LOGIC
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Compile Messages
    full_messages = [{"role": "system", "content": system_instruction}] + st.session_state.messages

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model_option,
                messages=full_messages,
                temperature=creativity,
                stream=True,
                max_tokens=2048 # Increased for smarter/longer answers
            )
            response = st.write_stream(generate_chat_responses(stream))
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
