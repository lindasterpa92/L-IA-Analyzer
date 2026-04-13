import streamlit as st
import google.generativeai as genai

# Configurazione chiave
genai.configure(api_key="AIzaSyAgIXxz2h6c2j_87yzuJz9SSpIZjuNN7JM")

# USIAMO IL MODELLO PIÙ COMPATIBILE IN ASSOLUTO
# Questo modello non fallisce mai il collegamento
model = genai.GenerativeModel('gemini-1.0-pro')

st.title("⚽ Il Socio Serie A")

# Inizializzazione memoria
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra i messaggi precedenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente
if prompt := st.chat_input("Socio, chi vince oggi?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Istruzione per farlo parlare come me
            istruzione_personalita = "Rispondi come un esperto di calcio simpatico e brillante: "
            response = model.generate_content(istruzione_personalita + prompt)
            
            risposta_testo = response.text
            st.markdown(risposta_testo)
            st.session_state.messages.append({"role": "assistant", "content": risposta_testo})
        except Exception as e:
            st.error(f"Errore tecnico: {e}")
