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
    # Carichiamo i file ignorando gli errori di riga
    lista_df = [pd.read_csv(f, encoding='latin1', header=None, on_bad_lines='skip') for f in file_csv]
    return pd.concat(lista_df, ignore_index=True)

db = carica_dati()

if db is not None:
    # Trasformiamo le colonne 1 e 2 in testo "puro" per evitare errori
    db[1] = db[1].astype(str)
    db[2] = db[2].astype(str)
    
    # Creiamo la lista squadre prendendo solo nomi validi
    squadre = sorted([s for s in db[1].unique() if s != 'nan' and len(s) > 1])

    col1, col2 = st.columns(2)
    with col1:
        casa = st.selectbox("Scegli squadra in casa", squadre)
    with col2:
        ospite = st.selectbox("Scegli squadra ospite", squadre)

    if st.button("PREVEDI RISULTATO"):
        dati_casa = db[db[1] == casa]
        dati_ospite = db[db[2] == ospite]

        # Convertiamo i gol in numeri (colonne 3 e 4)
        m_casa = pd.to_numeric(dati_casa[3], errors='coerce').mean()
        m_ospite = pd.to_numeric(dati_ospite[4], errors='coerce').mean()

        if pd.isna(m_casa) or pd.isna(m_ospite):
            st.error("Dati gol non trovati. Sicura che i gol siano nelle colonne 3 e 4?")
            # Mostriamo un'anteprima per capire dove sono i gol
            st.write("Anteprima dati per aiutarti:")
            st.dataframe(dati_casa.head(1))
        else:
            st.balloons()
            st.metric(label=f"Pronostico {casa}", value=f"{m_casa:.1f}")
            st.metric(label=f"Pronostico {ospite}", value=f"{m_ospite:.1f}")
            
            somma = m_casa + m_ospite
            if somma > 2.5:
                st.success("CONSIGLIO: OVER 2.5 🔥")
            else:
                st.info("CONSIGLIO: UNDER 2.5 🛡️")
else:
    st.warning("⚠️ Non trovo la cartella 'dati' o i file .csv su GitHub!")