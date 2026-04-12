import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="Linda IA", page_icon="⚽")
st.title("⚽ Linda's Football Intelligence")

@st.cache_data
def carica_dati():
    percorso = os.path.join("dati", "*.csv")
    file_csv = glob.glob(percorso)
    if not file_csv:
        return None
    lista_df = []
    for f in file_csv:
        try:
            # Carichiamo il file forzando tutto come testo all'inizio
            df = pd.read_csv(f, encoding='latin1', header=None, dtype=str)
            lista_df.append(df)
        except:
            continue
    return pd.concat(lista_df, ignore_index=True) if lista_df else None

db = carica_dati()

if db is not None:
    # Pulizia profonda: eliminiamo i valori nulli e convertiamo in stringa
    db[1] = db[1].fillna('').astype(str)
    db[2] = db[2].fillna('').astype(str)
    
    # Prendiamo le squadre: solo se il nome non è vuoto e non è 'nan'
    lista_squadre = db[1].unique().tolist()
    squadre = sorted([s for s in lista_squadre if s.strip() and s.lower() != 'nan'])

    col1, col2 = st.columns(2)
    with col1:
        casa = st.selectbox("Scegli squadra in casa", squadre)
    with col2:
        ospite = st.selectbox("Scegli squadra ospite", squadre)

    if st.button("PREVEDI RISULTATO"):
        dati_casa = db[db[1] == casa]
        dati_ospite = db[db[2] == ospite]

        # Convertiamo i gol (colonne 3 e 4) in numeri solo ora che ci servono
        m_casa = pd.to_numeric(dati_casa[3], errors='coerce').mean()
        m_ospite = pd.to_numeric(dati_ospite[4], errors='coerce').mean()

        if pd.isna(m_casa) or pd.isna(m_ospite):
            st.error("Dati gol non trovati nelle colonne 3 e 4.")
            # Ti mostro i dati così capiamo dove sono i gol
            st.write("Aiutami a capire: dove vedi i gol in questa riga?")
            st.table(dati_casa.head(1))
        else:
            st.balloons()
            st.subheader(f"Pronostico: {casa} {m_casa:.1f} - {m_ospite:.1f} {ospite}")
            
            somma = m_casa + m_ospite
            if somma > 2.5:
                st.success("CONSIGLIO: OVER 2.5 🔥")
            else:
                st.info("CONSIGLIO: UNDER 2.5 🛡️")
else:
    st.warning("⚠️ Controlla la cartella 'dati' su GitHub: deve contenere i file .csv")