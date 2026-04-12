import streamlit as st
import pandas as pd
import glob
import os

st.title("⚽ Linda's Football Intelligence")

# 1. CARICHIAMO I DATI
@st.cache_data
def carica_dati():
    percorso = os.path.join("dati", "*.csv")
    file_csv = glob.glob(percorso)
    if not file_csv: return None
    lista = [pd.read_csv(f, encoding='latin1', header=None, dtype=str) for f in file_csv]
    return pd.concat(lista, ignore_index=True)

db = carica_dati()

if db is not None:
    # 2. IDENTIFICHIAMO LE COLONNE (Semplificato)
    # Colonna 0 = ID o Data, Colonna 1 = Squadra Casa, Colonna 2 = Squadra Ospite
    # Colonna 3 = Gol Casa, Colonna 4 = Gol Ospite
    
    squadre = sorted(db[1].unique().tolist())

    col1, col2 = st.columns(2)
    with col1:
        casa = st.selectbox("Squadra in Casa", squadre)
    with col2:
        ospite = st.selectbox("Squadra Ospite", squadre)

    if st.button("PREVEDI RISULTATO"):
        # Filtriamo le partite delle due squadre
        f_casa = db[db[1] == casa]
        f_ospite = db[db[2] == ospite]
        
        # Calcoliamo la media gol (usando le colonne 3 e 4)
        m_casa = pd.to_numeric(f_casa[3], errors='coerce').mean()
        m_ospite = pd.to_numeric(f_ospite[4], errors='coerce').mean()

        if pd.isna(m_casa) or pd.isna(m_ospite):
            st.error("Dati non trovati. Prova a cambiare squadre!")
        else:
            st.balloons()
            st.header(f"Pronostico: {m_casa:.1f} - {m_ospite:.1f}")
            
            if (m_casa + m_ospite) > 2.5:
                st.success("CONSIGLIO: OVER 2.5 🔥")
            else:
                st.info("CONSIGLIO: UNDER 2.5 🛡️")
else:
    st.error("Carica i file CSV nella cartella 'dati' su GitHub!")