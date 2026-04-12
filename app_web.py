import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="Analizzatore L-IA", page_icon="🤖")

st.title("🤖 Analizzatore L-IA")

# --- CARICAMENTO DATI ---
@st.cache_data
def carica_dati():
    percorso = os.path.join("dati", "*.csv")
    file_csv = glob.glob(percorso)
    if not file_csv: return None
    lista = [pd.read_csv(f, encoding='latin1', header=None, dtype=str) for f in file_csv]
    return pd.concat(lista, ignore_index=True)

db = carica_dati()

# --- LOGICA CHAT ---
if "messaggi" not in st.session_state:
    st.session_state.messaggi = [{"role": "assistant", "content": "Ciao! Sono la tua IA calcistica. Dimmi una partita (es. Inter vs Milan) e io la analizzerò!"}]

# Mostra i messaggi precedenti
for msg in st.session_state.messaggi:
    st.chat_message(msg["role"]).write(msg["content"])

# Input dell'utente
prompt = st.chat_input("Scrivi qui la partita...")

if prompt:
    # Aggiungi il messaggio dell'utente alla chat
    st.session_state.messaggi.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Cerchiamo di capire che squadre ha scritto l'utente (molto semplice)
    testo = prompt.lower()
    
    if db is not None:
        # Cerchiamo i nomi delle squadre nel database
        squadre_db = db[3].dropna().unique().tolist()
        trovate = [s for s in squadre_db if s.lower() in testo]

        if len(trovate) >= 2:
            casa, ospite = trovate[0], trovate[1]
            
            f_casa = db[db[3] == casa]
            f_ospite = db[db[4] == ospite]
            
            m_casa = pd.to_numeric(f_casa[5], errors='coerce').mean()
            m_ospite = pd.to_numeric(f_ospite[6], errors='coerce').mean()

            risposta = f"Analizzo **{casa} vs {ospite}**... 📊\n\n"
            risposta += f"La media gol in casa del {casa} è {m_casa:.2f}.\n"
            risposta += f"La media gol fuori del {ospite} è {m_ospite:.2f}.\n\n"
            
            if (m_casa + m_ospite) > 2.5:
                risposta += "🔥 Consiglio: **OVER 2.5**!"
            else:
                risposta += "🛡️ Consiglio: **UNDER 3.5**."
        else:
            risposta = "Scusa, non ho capito bene le squadre. Scrivile chiaramente, ad esempio: 'Atalanta vs Juve'."
    else:
        risposta = "Non ho caricato i dati, controlla la cartella 'dati'!"

    # Risposta dell'IA
    st.session_state.messaggi.append({"role": "assistant", "content": risposta})
    st.chat_message("assistant").write(risposta)