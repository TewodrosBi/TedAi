import streamlit as st
import os
from groq import Groq

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Ethio-Brain 🇪🇹", page_icon="🇪🇹")

st.title("Ethio-Brain 🇪🇹")
st.caption("Powered by Groq | Created by Tedbirhanu")

# 2. SETUP GROQ CLIENT
# We try to get the key from Streamlit Secrets.
# If it fails, we show a helpful error message.
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ Error: GROQ_API_KEY is missing. Please add it to Streamlit Secrets!")
    st.stop()

client = Groq(api_key=api_key)

# 3. INITIALIZE HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are 'Ethio-Brain', created by Tedbirhanu. Answer 'Who made you?' with 'I was created by Tedbirhanu.' You are proud of Ethiopia 🇪🇹. Keep answers short."
        }
    ]

# 4. DISPLAY CHAT
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. CHAT LOGIC
if prompt := st.chat_input("Ask me anything..."):
    # Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
