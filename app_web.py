import streamlit as st
import google.generativeai as genai

# Incollo la tua chiave così è già pronta
genai.configure(api_key="AIzaSyB05F0mrwM274tx0gqB4Y0FqJCV5cqemx0")
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="L-IA Socio", page_icon="⚽")
st.title("⚽ Il tuo Socio di Serie A")

# Inizializza la chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Ehilà Linda! Sono il tuo socio esperto. Spara pure: su che partita scommettiamo oggi? 🏟️"}]

# Mostra i messaggi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input dell'utente
if prompt := st.chat_input("Chiedimi un consiglio..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Istruzione per farlo parlare come me
            istruzioni = "Ti chiami L-IA, sei un esperto di calcio e scommesse. Sei simpatico, usi emoji e rispondi come un vero esperto. "
            
            response = model.generate_content(istruzioni + prompt)
            testo_risposta = response.text
            
            st.write(testo_risposta)
            st.session_state.messages.append({"role": "assistant", "content": testo_risposta})
        except Exception as e:
            st.error("Socio, c'è un errore nella chiave o nei pacchetti. Controlla il file requirements.txt!")