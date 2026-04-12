import streamlit as st
import pandas as pd
import glob
import os

# Nome dell'app
st.set_page_config(page_title="Analizzatore L-IA", page_icon="⚽")
st.title("⚽ Analizzatore L-IA")

@st.cache_data
def carica_dati():
    percorso = os.path.join("dati", "*.csv")
    file_csv = glob.glob(percorso)
    if not file_csv:
        return None
    lista_df = []
    for f in file_csv:
        try:
            df = pd.read_csv(f, encoding='latin1', header=None, dtype=str)
            lista_df.append(df)
        except:
            continue
    return pd.concat(lista_df, ignore_index=True) if lista_df else None

db = carica_dati()

if db is not None:
    # --- MODIFICA QUI ---
    # Usiamo la colonna 2 per la Casa e la 3 per l'Ospite (saltiamo la data)
    db[2] = db[2].fillna("Sconosciuta").astype(str)
    db[3] = db[3].fillna("Sconosciuta").astype(str)
    
    squadre = sorted([s for s in db[2].unique() if s != "Sconosciuta"])

    col1, col2 = st.columns(2)
    with col1:
        casa = st.selectbox("Squadra in Casa", squadre)
    with col2:
        ospite = st.selectbox("Squadra Ospite", squadre)

    if st.button("GENERA PRONOSTICO"):
        f_casa = db[db[2] == casa]
        f_ospite = db[db[3] == ospite]
        
        # I gol dovrebbero essere nelle colonne 4 e 5
        m_casa = pd.to_numeric(f_casa[4], errors='coerce').mean()
        m_ospite = pd.to_numeric(f_ospite[5], errors='coerce').mean()

        if pd.isna(m_casa) or pd.isna(m_ospite):
            st.error("Dati gol non trovati. Prova a cambiare squadre!")
        else:
            st.balloons()
            st.subheader(f"Risultato stimato: {m_casa:.1f} - {m_ospite:.1f}")
            
            somma = m_casa + m_ospite
            if somma > 2.5:
                st.success("CONSIGLIO: OVER 2.5 🔥")
            else:
                st.info("CONSIGLIO: UNDER 2.5 🛡️")
else:
    st.warning("⚠️ Carica i file .csv nella cartella 'dati' su GitHub!")