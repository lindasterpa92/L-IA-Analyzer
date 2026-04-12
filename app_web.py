import streamlit as st
import pandas as pd
import glob
import os

# Configurazione Pagina
st.set_page_config(page_title="Analizzatore L-IA", page_icon="🤖")

# --- INTERFACCIA STILE ASSISTENTE ---
st.title("🤖 Analizzatore L-IA")
st.markdown("""
### Ciao Linda! 👋 
Benvenuta nel tuo assistente personale per i pronostici. 
Scegli le partite di oggi e io calcolerò per te le probabilità basandomi sui dati storici!
""")

@st.cache_data
def carica_dati():
    percorso = os.path.join("dati", "*.csv")
    file_csv = glob.glob(percorso)
    if not file_csv: return None
    lista = [pd.read_csv(f, encoding='latin1', header=None, dtype=str) for f in file_csv]
    return pd.concat(lista, ignore_index=True)

db = carica_dati()

if db is not None:
    # PULIZIA: Saltiamo Data (0), Orario (1), Stato (2) 
    # Proviamo a prendere le squadre dalla colonna 3 e 4
    db[3] = db[3].fillna("Vuoto").astype(str)
    db[4] = db[4].fillna("Vuoto").astype(str)
    
    squadre = sorted([s for s in db[3].unique() if s != "Vuoto" and ":" not in s])

    st.info("✍️ **Inserisci i dati della partita:**")
    col1, col2 = st.columns(2)
    with col1:
        casa = st.selectbox("Chi gioca in casa?", squadre)
    with col2:
        ospite = st.selectbox("Chi gioca fuori casa?", squadre)

    if st.button("✨ ELABORA PRONOSTICO"):
        f_casa = db[db[3] == casa]
        f_ospite = db[db[4] == ospite]
        
        # I gol dovrebbero essere nelle colonne 5 e 6
        m_casa = pd.to_numeric(f_casa[5], errors='coerce').mean()
        m_ospite = pd.to_numeric(f_ospite[6], errors='coerce').mean()

        if pd.isna(m_casa) or pd.isna(m_ospite):
            st.warning("⚠️ Scusa Linda, per queste squadre non ho abbastanza dati nelle colonne dei gol.")
        else:
            st.balloons()
            st.markdown(f"### 📋 Analisi completata per **{casa} vs {ospite}**")
            
            c1, c2 = st.columns(2)
            c1.metric(f"Media Gol {casa}", f"{m_casa:.2f}")
            c2.metric(f"Media Gol {ospite}", f"{m_ospite:.2f}")
            
            somma = m_casa + m_ospite
            if somma > 2.5:
                st.success(f"🔥 **Il mio consiglio:** Questa sembra una partita da **OVER 2.5** (Totale stimato: {somma:.1f})")
            else:
                st.info(f"🛡️ **Il mio consiglio:** Vedo una partita tattica, suggerisco **UNDER 3.5**")
else:
    st.error("Linda, non trovo i file CSV! Controlla la cartella 'dati'.")