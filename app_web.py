import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="IA Football Analyzer", page_icon="⚽")

st.title("⚽ IA Football Analyzer Online")
st.write("Analizza i match dai tuoi database CSV direttamente dal telefono.")

# Caricamento dati
@st.cache_data
def carica_dati():
    percorso_dati = os.path.join("dati", "*.csv")
    tutti_i_file = glob.glob(percorso_dati)
    lista = [pd.read_csv(f, encoding='latin1') for f in tutti_i_file]
    return pd.concat(lista, ignore_index=True) if lista else None

db = carica_dati()

if db is not None:
    # Menu a tendina con le squadre (ordinate alfabeticamente)
    squadre = sorted(db['HomeTeam'].unique())
    
    col1, col2 = st.columns(2)
    with col1:
        casa = st.selectbox("Squadra in Casa", squadre)
    with col2:
        ospite = st.selectbox("Squadra Ospite", squadre)

    if st.button("GENERA PRONOSTICO"):
        f_casa = db[db['HomeTeam'] == casa]
        f_ospite = db[db['AwayTeam'] == ospite]
        
        m_casa = f_casa['FTHG'].mean()
        m_ospite = f_ospite['FTAG'].mean()
        
        st.success(f"Risultato Stimato: {casa} {m_casa:.1f} - {m_ospite:.1f} {ospite}")
        
        if m_casa + m_ospite > 2.5:
            st.warning("🔥 Consiglio: OVER 2.5")
        else:
            st.info("🛡️ Consiglio: UNDER 3.5")
else:
    st.error("Carica la cartella 'dati' con i file CSV per iniziare!")