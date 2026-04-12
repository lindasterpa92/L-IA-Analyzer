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
            # Carichiamo forzando le colonne 1 e 2 come stringhe (testo)
            df = pd.read_csv(f, encoding='latin1', header=None)
            # Pulizia: eliminiamo righe completamente vuote
            df = df.dropna(subset=[1, 2])
            lista.append(df)
        except:
            continue
    return pd.concat(lista, ignore_index=True) if lista else None

db = carica_dati()

if db is not None:
    try:
        # Trasformiamo tutto in stringa e togliamo eventuali spazi prima di ordinare
        db[1] = db[1].astype(str).str.strip()
        db[2] = db[2].astype(str).str.strip()
        
        # Prendiamo solo i nomi unici che non siano "nan" o vuoti
        squadre = sorted([s for s in db[1].unique() if s.lower() != 'nan' and s != ''])
        
        col1, col2 = st.columns(2)
        with col1:
            casa = st.selectbox("Squadra in Casa", squadre)
        with col2:
            ospite = st.selectbox("Squadra Ospite", squadre)

        if st.button("GENERA PRONOSTICO"):
            f_casa = db[db[1] == casa]
            f_ospite = db[db[2] == ospite]
            
            # Convertiamo i gol (colonne 3 e 4) in numeri, ignorando gli errori
            m_casa = pd.to_numeric(f_casa[3], errors='coerce').mean()
            m_ospite = pd.to_numeric(f_ospite[4], errors='coerce').mean()
            
            if pd.isna(m_casa) or pd.isna(m_ospite):
                st.error("Ops! Non ho abbastanza dati numerici per calcolare la media.")
            else:
                st.success(f"Risultato Stimato: {casa} {m_casa:.1f} - {m_ospite:.1f} {ospite}")
                
                somma = m_casa + m_ospite
                if somma > 2.5:
                    st.warning("🔥 Suggerimento: OVER 2.5")
                else:
                    st.info("🛡️ Suggerimento: UNDER 3.5")
                    
    except Exception as e:
        st.error(f"Errore tecnico: {e}")
else:
    st.warning("⚠️ Non ho trovato i file CSV nella cartella 'dati'.")