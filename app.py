import streamlit as st
import os
from groq import Groq

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Ethio-Brain 🇪🇹", page_icon="🇪🇹")

st.title("Ethio-Brain 🇪🇹")
st.caption("Powered by Groq | Created by Tedbirhanu")

# 2. SETUP GROQ
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ Error: GROQ_API_KEY is missing in Secrets!")
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

# 4. DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. GENERATOR FUNCTION (The Fix 🛠️)
# This unwraps the "messy" JSON and gives us clean text
def generate_chat_responses(chat_completion):
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# 6. CHAT LOGIC
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Create the stream
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            stream=True,
        )
        
        # Use st.write_stream with our cleaner function
        response = st.write_stream(generate_chat_responses(stream))
    
    st.session_state.messages.append({"role": "assistant", "content": response})
