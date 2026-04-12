import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="Linda's IA", page_icon="⚽")
st.title("⚽ Linda's Football Intelligence")

@st.cache_data
def carica_dati():
    percorso_dati = os.path.join("dati", "*.csv")
    tutti_i_file = glob.glob(percorso_dati)
    if not tutti_i_file:
        return None
    
    lista = []
    for f in tutti_i_file:
        try:
            # Carichiamo il file senza intestazione (header=None)
            df = pd.read_csv(f, encoding='latin1', header=None)
            lista.append(df)
        except:
            continue
    return pd.concat(lista, ignore_index=True) if lista else None

db = carica_dati()

if db is not None:
    # Assegniamo noi i nomi alle colonne in base alla posizione
    # 1 è la casa, 2 è l'ospite, 3 gol casa, 4 gol ospite
    try:
        squadre = sorted(db[1].unique()) 
        
        col1, col2 = st.columns(2)
        with col1:
            casa = st.selectbox("Squadra in Casa", squadre)
        with col2:
            ospite = st.selectbox("Squadra Ospite", squadre)

        if st.button("GENERA PRONOSTICO"):
            # Filtriamo usando i numeri delle colonne
            f_casa = db[db[1] == casa]
            f_ospite = db[db[2] == ospite]
            
            # Calcoliamo la media gol (colonne 3 e 4)
            m_casa = pd.to_numeric(f_casa[3], errors='coerce').mean()
            m_ospite = pd.to_numeric(f_ospite[4], errors='coerce').mean()
            
            if pd.isna(m_casa) or pd.isna(m_ospite):
                st.error("Dati insufficienti per queste squadre.")
            else:
                st.success(f"Risultato Stimato: {casa} {m_casa:.1f} - {m_ospite:.1f} {ospite}")
                
                somma = m_casa + m_ospite
                if somma > 2.5:
                    st.warning("🔥 Suggerimento: OVER 2.5")
                else:
                    st.info("🛡️ Suggerimento: UNDER 3.5")
    except Exception as e:
        st.error(f"C'è un problema con la struttura dei file: {e}")
else:
    st.warning("⚠️ Non ho trovato i file CSV. Assicurati che siano nella cartella 'dati' su GitHub!")