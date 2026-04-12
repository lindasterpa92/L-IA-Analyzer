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
    lista_df = [pd.read_csv(f, encoding='latin1', header=None) for f in file_csv]
    return pd.concat(lista_df, ignore_index=True)

db = carica_dati()

if db is not None:
    # Pulizia: teniamo solo le colonne che hanno i nomi delle squadre (solitamente colonna 1 e 2)
    db[1] = db[1].astype(str)
    db[2] = db[2].astype(str)
    squadre = sorted([s for s in db[1].unique() if len(s) > 2 and s.lower() != 'nan'])

    col1, col2 = st.columns(2)
    with col1:
        casa = st.selectbox("Scegli squadra in casa", squadre)
    with col2:
        ospite = st.selectbox("Scegli squadra ospite", squadre)

    if st.button("PREVEDI RISULTATO"):
        # Cerchiamo i gol: prendiamo le colonne che hanno i numeri (di solito la 3 e la 4)
        dati_casa = db[db[1] == casa]
        dati_ospite = db[db[2] == ospite]

        # Proviamo a indovinare le colonne dei gol (3 e 4 sono le più comuni)
        try:
            media_casa = pd.to_numeric(dati_casa[3], errors='coerce').mean()
            media_ospite = pd.to_numeric(dati_ospite[4], errors='coerce').mean()

            if pd.isna(media_casa) or pd.isna(media_ospite):
                st.error("I dati in questo file sono salvati in un modo strano. Prova a controllare se le squadre sono giuste!")
            else:
                st.balloons() # Un po' di festa!
                st.header(f"Pronostico: {media_casa:.1f} - {media_ospite:.1f}")
                
                if (media_casa + media_ospite) > 2.5:
                    st.success("Consiglio: OVER 2.5 🎯")
                else:
                    st.info("Consiglio: UNDER 2.5 🛡️")
        except:
            st.error("C'è un problema con la lettura dei gol nei tuoi file.")
else:
    st.warning("⚠️ Non vedo i file! Controlla che dentro GitHub ci sia la cartella 'dati' con i file .csv")