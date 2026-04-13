import streamlit as st
import google.generativeai as genai

# La tua chiave
genai.configure(api_key="AIzaSyAgIXxz2h6c2j_87yzuJz9SSpIZjuNN7JM")

# PROVIAMO IL NOME MODELLO PIÙ COMPATIBILE
model = genai.GenerativeModel('models/gemini-1.5-flash')

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
            # Chiamata al modello
            res = model.generate_content(prompt)
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
        except Exception as e:
            # Se dà ancora errore, stampiamo un consiglio
            st.error(f"Errore tecnico: {e}")
            st.info("Socio, stiamo sistemando i cavi della connessione. Riprova tra un attimo!")
