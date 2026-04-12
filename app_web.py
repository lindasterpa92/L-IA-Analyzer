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
            # Legge tutto come testo per non fare confusione
            df = pd.read_csv(f, encoding='latin1', header=None, dtype=str)
            lista_df.append(df)
        except:
            continue
    return pd.concat(lista_df, ignore_index=True) if lista_df else None

db = carica_dati()

if db is not None:
    # Pulizia: togliamo le righe vuote e trasformiamo in parole
    db = db.dropna(subset=[1, 2]) 
    
    # Se vedi ancora DATE invece di nomi, cambia l'1 con 2 e il 2 con 3 qui sotto:
    squadre = sorted(db[1].unique().astype(str))

    col1, col2 = st.columns(2)
    with col1:
        casa = st.selectbox("Squadra in Casa", squadre)
    with col2:
        ospite = st.selectbox("Squadra Ospite", squadre)

    if st.button("GENERA PRONOSTICO"):
        # Filtra le partite
        f_casa = db[db[1] == casa]
        f_ospite = db[db[2] == ospite]
        
        # Converte i gol in numeri (colonne 3 e 4) e fa la media
        m_casa = pd.to_numeric(f_casa[3], errors='coerce').mean()
        m_ospite = pd.to_numeric(f_ospite[4], errors='coerce').mean()

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