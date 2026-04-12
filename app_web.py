import streamlit as st
import pandas as pd
import glob
import os

# Configurazione Pagina
st.set_page_config(page_title="Analizzatore L-IA", page_icon="🤖")

# --- INTERFACCIA ASSISTENTE ---
st.title("🤖 Analizzatore L-IA")

# Messaggio di benvenuto universale
st.markdown("""
### Benvenuto nel tuo Assistente Virtuale! 👋 
Sono qui per aiutarti ad analizzare le partite di calcio. 
Utilizzo i dati storici per calcolare le medie gol e suggerirti il pronostico più probabile.
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
    # Pulizia colonne (saltiamo i primi campi inutili)
    db[3] = db[3].fillna("Vuoto").astype(str)
    db[4] = db[4].fillna("Vuoto").astype(str)
    
    # Filtriamo via orari o date rimaste nei dati
    squadre = sorted([s for s in db[3].unique() if s != "Vuoto" and ":" not in s and "/" not in s])

    st.divider() # Una linea elegante di separazione
    
    st.subheader("✍️ Configura la Partita")
    col1, col2 = st.columns(2)
    with col1:
        casa = st.selectbox("Squadra in Casa", squadre)
    with col2:
        ospite = st.selectbox("Squadra Ospite", squadre)

    if st.button("✨ ELABORA PRONOSTICO"):
        if casa == ospite:
            st.warning("⚠️ Hai selezionato la stessa squadra per entrambi i ruoli. Scegli due squadre diverse!")
        else:
            f_casa = db[db[3] == casa]
            f_ospite = db[db[4] == ospite]
            
            # Calcolo medie (colonne 5 e 6 per i gol)
            m_casa = pd.to_numeric(f_casa[5], errors='coerce').mean()
            m_ospite = pd.to_numeric(f_ospite[6], errors='coerce').mean()

            if pd.isna(m_casa) or pd.isna(m_ospite):
                st.error("Scusa, non ho abbastanza dati storici per generare un calcolo preciso su questa coppia.")
            else:
                st.balloons()
                st.markdown(f"## 📋 Analisi: **{casa} vs {ospite}**")
                
                # Box colorati per le medie
                c1, c2 = st.columns(2)
                c1.metric(f"Potenziale {casa}", f"{m_casa:.2f} gol")
                c2.metric(f"Potenziale {ospite}", f"{m_ospite:.2f} gol")
                
                somma = m_casa + m_ospite
                
                st.markdown("---")
                if somma > 2.5:
                    st.success(f"🔥 **IL MIO CONSIGLIO:** Questa partita ha un alto potenziale offensivo. Suggerisco **OVER 2.5** (Media totale: {somma:.2f})")
                else:
                    st.info(f"🛡️ **IL MIO CONSIGLIO:** Le statistiche prevedono una partita chiusa. Suggerisco **UNDER 3.5** (Media totale: {somma:.2f})")
else:
    st.error("⚠️ Errore: Non sono riuscito a trovare il database dei file CSV.")