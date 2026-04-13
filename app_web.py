import streamlit as st
import google.generativeai as genai

# La tua chiave
genai.configure(api_key="AIzaSyAgIXxz2h6c2j_87yzuJz9SSpIZjuNN7JM")

# MODELLO AGGIORNATO ALLA VERSIONE DEFINITIVA:
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.title("⚽ Il Socio Serie A")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Socio, chi vince oggi?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Istruzione di base
            res = model.generate_content("Sei un esperto di calcio Serie A. Rispondi a: " + prompt)
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
        except Exception as e:
            st.error(f"Errore: {e}")