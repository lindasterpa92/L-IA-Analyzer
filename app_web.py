import streamlit as st
import google.generativeai as genai

# La tua chiave è già qui dentro
genai.configure(api_key="AIzaSyAgIXxz2h6c2j_87yzuJz9SSpIZjuNN7JM")
model = genai.GenerativeModel('gemini-pro')

st.title("⚽ Il Socio Serie A")

if prompt := st.chat_input("Chiedimi un consiglio..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        # Chiediamo all'IA di risponderti
        res = model.generate_content("Sei un esperto di calcio, rispondi a: " + prompt)
        st.write(res.text)