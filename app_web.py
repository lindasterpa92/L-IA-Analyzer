import streamlit as st
import google.generativeai as genai

# Configurazione IA
genai.configure(api_key="AIzaSyB05F0mrwM274tx0gqB4Y0FqJCV5cqemx0")
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="L-IA Socio Serie A", page_icon="⚽")
st.title("⚽ L-IA: L'Esperto Totale")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Ehilà! Sono pronto. Ho analizzato le ultime di Serie A. Vuoi sapere su chi scommettere o parliamo dei big match? 🏟️"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Chiedimi un consiglio o info sulla Serie A..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # AGGIUNGIAMO LE INFO EXTRA QUI DENTRO
            istruzioni_serie_a = (
                "Tu sei L-IA, un super esperto di calcio italiano della stagione 2025/2026. "
                "Conosci tutto: la classifica, chi segna di più e chi è in crisi. "
                "Se Linda ti chiede su chi scommettere, analizza lo stato di forma delle squadre. "
                "Usa un tono da bar sport: esperto, simpatico, deciso e pieno di emoji. "
                "Consiglia sempre una giocata specifica (es. Over 2.5, 1X, Goal) e spiega perché."
            )
            
            response = model.generate_content(istruzioni_serie_a + "\n\nDomanda: " + prompt)
            risposta = response.text
            
            st.write(risposta)
            st.session_state.messages.append({"role": "assistant", "content": risposta})
        except Exception as e:
            st.error("Socio, ho un piccolo blackout! Prova a ricaricare la pagina.")