import streamlit as st
import os
import datetime
from groq import Groq

# 1. PAGE SETUP (Wide & Professional)
st.set_page_config(
    page_title="Ethio-Brain 🇪🇹",
    page_icon="🇪🇹",
    layout="wide"
)

# 2. SIDEBAR CONTROLS
with st.sidebar:
    st.title("🇪🇹 Ethio-Brain Settings")
    
    # POWER SWITCH: Defaulting to Llama 3.3 (The Latest)
    model_option = st.selectbox(
        "🧠 Brain Engine:",
        ("llama-3.3-70b-versatile", "llama-3.1-8b-instant"),
        index=0, # Defaults to the 70B (Smartest) model
        help="Llama 3.3 is the latest & smartest. 3.1 is faster."
    )
    
    # CREATIVITY KNOB
    creativity = st.slider(
        "🎨 Creativity:", 
        0.0, 1.0, 0.6,
        help="Higher = More Creative. Lower = More Logical."
    )
    
    # RESET BUTTON
    if st.button("🗑️ Reset Chat", type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    # STATUS INDICATORS
    st.markdown("---")
    st.success(f"⚡ Online: {model_option}")
    st.caption(f"📅 Server Time: {datetime.datetime.now().strftime('%H:%M')}")

# 3. MAIN TITLE
st.title("Ethio-Brain 🇪🇹")
st.markdown("#### The Advanced AI Assistant | Powered by Llama 3.3")

# 4. CONNECT TO GROQ
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("❌ Error: API Key missing in Streamlit Secrets!")
    st.stop()

# 5. DYNAMIC TIME INJECTION ⏰
# This captures the EXACT current time/date every time you hit enter.
current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
current_time = datetime.datetime.now().strftime("%I:%M %p")

system_instruction = f"""
You are 'Ethio-Brain', the most advanced Ethiopian AI.

LIVE DATA:
- Today's Date: {current_date}
- Current Time: {current_time}

YOUR IDENTITY:
1. Creator: You were created by Tedbirhanu. (Never say Meta or Groq).
2. Heritage: You are proud of Ethiopia 🇪🇹.
3. Capabilities: Expert in Python, React Native, and General Knowledge.

BEHAVIOR:
- Be concise but intelligent.
- If asked about the date/time, use the 'LIVE DATA' above.
"""

# 6. MEMORY MANAGEMENT
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. DISPLAY CHAT
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. RESPONSE CLEANER (Removes raw JSON junk)
def generate_chat_responses(chat_completion):
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# 9. CHAT LOGIC
if prompt := st.chat_input("Ask me anything..."):
    
    # Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build the Brain Packet (System + History)
    full_messages = [{"role": "system", "content": system_instruction}] + st.session_state.messages

    # Generate Smart Response
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model_option,
                messages=full_messages,
                temperature=creativity,
                stream=True,
                max_tokens=1024
            )
            response = st.write_stream(generate_chat_responses(stream))
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"⚠️ Network Error: {str(e)}")
