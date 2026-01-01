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

# 2. SIDEBAR CONTROLS ⚙️
with st.sidebar:
    st.title("🇪🇹 Ethio-Brain Controls")
    
    # FEATURE 1: SMART MODES
    brain_mode = st.selectbox(
        "🎓 Select Persona:",
        ("General Assistant", "👨‍💻 Senior Developer", "🎓 Academic Tutor", "🇪🇹 Ethiopian Expert"),
        index=0
    )
    
    # FEATURE 2: MODEL RENAMING (The Fix 🛠️)
    # We show "Friendly Names" to user, but map them to "Real Names" for code.
    model_mapping = {
        "🏆 Pro (Smartest)": "llama-3.3-70b-versatile",
        "⚡ Fast (Speed)": "llama-3.1-8b-instant"
    }
    
    # The user sees keys ("Pro", "Fast")
    selected_friendly_name = st.selectbox(
        "🚀 Engine:",
        list(model_mapping.keys()),
        index=0
    )
    
    # We get the value ("llama-3.3...") for the API
    selected_model_id = model_mapping[selected_friendly_name]
    
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
st.markdown(f"#### Mode: **{brain_mode}** | Engine: **{selected_friendly_name}**")

# 4. SETUP GROQ
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("❌ Error: API Key is missing.")
    st.stop()

# 5. DEFINE SMART PERSONAS
current_time = datetime.datetime.now().strftime("%A, %B %d, %Y")

base_instruction = f"""
You are 'Ethio-Brain', created by Tedbirhanu.
Current Time: {current_time}.
"""

if brain_mode == "👨‍💻 Senior Developer":
    system_instruction = base_instruction + """
    ROLE: Senior Software Engineer.
    RULES: Write clean, commented, production-ready code. No fluff.
    """
elif brain_mode == "🎓 Academic Tutor":
    system_instruction = base_instruction + """
    ROLE: Patient Professor.
    RULES: Explain step-by-step. Use analogies. Be encouraging.
    """
elif brain_mode == "🇪🇹 Ethiopian Expert":
    system_instruction = base_instruction + """
    ROLE: Expert on Ethiopian History & Culture.
    RULES: Share deep knowledge about Ethiopia. Speak Amharic if asked.
    """
else:
    system_instruction = base_instruction + """
    ROLE: Helpful Assistant.
    RULES: Answer 'Who made you?' with 'I was created by Tedbirhanu.'
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

    full_messages = [{"role": "system", "content": system_instruction}] + st.session_state.messages

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=selected_model_id, # Uses the mapped ID (llama-3.3...)
                messages=full_messages,
                temperature=creativity,
                stream=True,
                max_tokens=2048
            )
            response = st.write_stream(generate_chat_responses(stream))
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
