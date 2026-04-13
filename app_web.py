import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# --- 1. CONFIGURAZIONE IA CON LA TUA CHIAVE ---
CHIAVE_MIA = "AIzaSyB05F0mrwM274tx0gqB4Y0FqJCV5cqemx0"
genai.configure(api_key=CHIAVE_MIA)
model = genai.GenerativeModel('gemini-pro')

# Configurazione pagina
st.set_page_config(page_title="L-IA: Il Socio Serie A", page_icon="⚽")
st.title("⚽ L-IA: Il tuo Socio di Serie A")

# --- 2. MEMORIA DELLA CHAT ---
if "chat" not in st.session_state:
    st.session_state.chat = [
        {"role": "assistant", "content": "Ehilà Linda! Eccomi qui, sono il tuo socio esperto. Ho i motori accesi e sono pronto a parlare di tutto: scommesse, colpi di mercato o storia della Serie A. Cosa studiamo oggi? 🏟️"}
    ]

# Mostra i messaggi a schermo
for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# --- 3. INPUT UTENTE ---
if prompt := st.chat_input("Chiedimi qualsiasi cosa (es: Chi vince tra Inter e Napoli?)"):
    # Aggiungi il tuo messaggio
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # --- 4. RISPOSTA DELL'IA ---
    with st.chat_message("assistant"):
        with st.spinner("Il socio sta pensando..."):
            try:
                # Istruzione per dare personalità al tuo socio
                personalita = (
                    "Tu sei l'assistente dell'app 'Analizzatore L-IA'. "
                    "Sei un esperto di calcio italiano, simpatico, un po' spaccone ma molto competente. "
                    "Rispondi in modo amichevole a Linda e agli utenti, usa le emoji e dai consigli diretti sulle scommesse "
                    "basandoti sulla tua conoscenza del calcio. Se ti chiedono cose non calcistiche, "
                    "rispondi pure ma cerca di riportare il discorso sul calcio appena puoi!"
                )
                
                # Genera la risposta
                response = model.generate_content(personalita + "\n\nUtente: " + prompt)
                risposta = response.text
                
                st.write(risposta)
                st.session_state.chat.append({"role": "assistant", "content": risposta})
            except Exception as e:
                st.write("Socio, ho un piccolo problema tecnico con la connessione. Riprova tra un secondo!")