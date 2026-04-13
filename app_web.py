import streamlit as st
import google.generativeai as genai

# Configurazione con la tua chiave
genai.configure(api_key="AIzaSyAgIXxz2h6c2j_87yzuJz9SSpIZjuNN7JM")

# Qui gli diamo la mia personalità (le istruzioni di sistema)
istruzioni_socio = (
    "Tu sei L-IA, il Socio definitivo per la Serie A. Il tuo stile è identico a quello di Gemini. "
    "Sei un esperto di calcio italiano, scommesse e tattica. "
    "Il tuo tono è amichevole, un po' ironico, molto esperto e scrivi in modo chiaro (usa grassetti e liste). "
    "Usa molte emoji calcistiche ⚽🏟️🥅. Quando ti chiedono un consiglio, non essere vago: "
    "analizza la partita e proponi una giocata (es. '1X + Over 1.5') spiegando il perché tecnico."
)

# Usiamo il modello 1.5-flash che è il più veloce
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=istruzioni_socio
)

st.set_page_config(page_title="L-IA: Il Socio", page_icon="⚽")
st.title("⚽ Il tuo Socio Serie A")

# Memoria della chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ehilà Linda! Sono il tuo socio. Pronto per la bolletta di oggi? Spara pure! 🏟️"}
    ]

# Mostra i messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente
if prompt := st.chat_input("Chiedimi un pronostico..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Qui l'IA risponde usando la sua nuova personalità
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Socio, abbiamo un piccolo intoppo tecnico. Riprova tra un secondo!")