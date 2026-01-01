import streamlit as st
import os
import datetime
from groq import Groq

# 1. PAGE CONFIGURATION 🎨
st.set_page_config(
    page_title="Ethio-Brain 🇪🇹",
    page_icon="🇪🇹",
    layout="wide"
)

# 2. SIDEBAR SETTINGS ⚙️
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Feature 1: Model Selection (In case 70B is too slow, you can switch back)
    model_option = st.selectbox(
        "Choose Brain Power:",
        ("llama-3.3-70b-versatile", "llama-3.1-8b-instant"),
        index=0,
        help="70B is Smarter. 8B is Faster."
    )
    
    # Feature 2: Creativity Slider
    creativity = st.slider(
        "Creativity Level:", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7,
        help="0.0 is strict/logical. 1.0 is creative/random."
    )
    
    # Feature 3: Clear History Button
    if st.button("🗑️ Clear Conversation", type="primary"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("Created by **Tedbirhanu**")
    st.caption("Powered by **Groq**")

# 3. MAIN INTERFACE 🇪🇹
st.title("Ethio-Brain 🇪🇹")
st.markdown("#### The Smartest Ethiopian AI Assistant")

# Feature 4: Time Awareness ⏰
current_time = datetime.datetime.now().strftime("%A, %B %d, %Y")

# 4. SETUP GROQ CLIENT
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ Error: GROQ_API_KEY is missing in Secrets!")
    st.stop()

client = Groq(api_key=api_key)

# 5. INITIALIZE HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# Update System Prompt Dynamically (to keep time current)
system_prompt = {
    "role": "system",
    "content": f"""
    You are 'Ethio-Brain', a highly advanced AI created by Tedbirhanu.
    
    CONTEXT:
    - Current Date: {current_time}
    
    IDENTITY RULES:
    1. If asked 'Who made you?', answer EXACTLY: 'I was created by Tedbirhanu.'
    2. You are proud of your Ethiopian heritage. 🇪🇹
    3. You are an Expert Senior Developer (Python, React Native, Streamlit).
    4. You are helpful, kind, and intelligent.
    """
}

# 6. FEATURE: QUICK ACTION BUTTONS ⚡
# Only show these if chat is empty
if len(st.session_state.messages) == 0:
    col1, col2, col3 = st.columns(3)
    if col1.button("🇪🇹 Ethiopian Fact"):
        st.session_state.messages.append({"role": "user", "content": "Tell me an interesting fact about Ethiopia."})
        st.rerun()
    if col2.button("🐍 Write Python Code"):
        st.session_state.messages.append({"role": "user", "content": "Write a simple Python script to calculate Fibonacci numbers."})
        st.rerun()
    if col3.button("😂 Tell a Joke"):
        st.session_state.messages.append({"role": "user", "content": "Tell me a funny joke!"})
        st.rerun()

# 7. DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. GENERATOR FUNCTION (Clean Output) 🧼
def generate_chat_responses(chat_completion):
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# 9. CHAT LOGIC
if prompt := st.chat_input("Ask me anything..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare Messages (System Prompt + History)
    full_messages = [system_prompt] + st.session_state.messages

    # Generate Response
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model_option, # Uses the slider selection
                messages=full_messages,
                temperature=creativity, # Uses the slider selection
                stream=True,
                max_tokens=1024
            )
            response = st.write_stream(generate_chat_responses(stream))
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
