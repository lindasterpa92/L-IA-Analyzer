import streamlit as st
import google.generativeai as genai

# La tua chiave aggiornata
genai.configure(api_key="AIzaSyAgIXxz2h6c2j_87yzuJz9SSpIZjuNN7JM")

# ABBIAMO CAMBIATO IL MODELLO QUI SOTTO:
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("⚽ Il Socio Serie A")

if prompt := st.chat_input("Chiedimi un consiglio..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Chiediamo all'IA di risponderti
            res = model.generate_content("Sei un esperto di calcio, rispondi a: " + prompt)
            st.write(res.text)
        except Exception as e:
            st.error(f"Errore: {e}")