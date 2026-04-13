import streamlit as st
import google.generativeai as genai

# Configurazione chiave
genai.configure(api_key="AIzaSyAgIXxz2h6c2j_87yzuJz9SSpIZjuNN7JM")

# Istruzioni di personalità
istruzioni = (
    "Sei L-IA, il Socio di Linda. Sei un esperto di Serie A simpatico e brillante. "
    "Usa grassetti ed emoji. Dai consigli chiari sulle scommesse."
)

# MODELLO STANDARD (Senza scritte extra che causano il 404)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=istruzioni
)

st.title("⚽ Il tuo Socio Serie A")

# Inizializzazione memoria chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra la cronologia
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente
if prompt := st.chat_input("Socio, su chi scommettiamo?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Chiamata diretta e pulita
            response = model.generate_content(prompt)
            # Salviamo e mostriamo la risposta
            risposta_testo = response.text
            st.markdown(risposta_testo)
            st.session_state.messages.append({"role": "assistant", "content": risposta_testo})
        except Exception as e:
            st.error(f"Errore tecnico: {e}")
