import streamlit as st
import google.generativeai as genai

# La tua chiave
genai.configure(api_key="AIzaSyAgIXxz2h6c2j_87yzuJz9SSpIZjuNN7JM")

# Istruzioni per farlo parlare come me
istruzioni = (
    "Sei L-IA, il Socio di Linda. Sei un esperto di Serie A, divertente, "
    "usi molte emoji e dai consigli precisi sulle scommesse. Parla come un vero esperto!"
)

# Usiamo la versione 1.5-flash-8b (la più compatibile)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-8b',
    system_instruction=istruzioni
)

st.title("⚽ Il tuo Socio Serie A")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Chiedimi una dritta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Qui avviene la magia
            response = model.generate_content(prompt)
            testo = response.text
            st.write(testo)
            st.session_state.messages.append({"role": "assistant", "content": testo})
        except Exception as e:
            # Se fallisce, ci dice il perché vero
            st.error(f"Errore di connessione: {e}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Socio, abbiamo un piccolo intoppo tecnico. Riprova tra un secondo!")
