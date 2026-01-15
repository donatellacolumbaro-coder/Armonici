import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configurazione della pagina
st.set_page_config(page_title="Laboratorio degli Armonici", layout="wide")

st.title("🎵 Laboratorio Interattivo degli Armonici")
st.markdown("""
Questa applicazione permette di esplorare la **serie armonica**. 
Scegli una frequenza fondamentale e attiva i suoi multipli per sentire come cambia il timbro del suono.
""")

# --- Sidebar: Parametri di Controllo ---
st.sidebar.header("Parametri Fondamentali")
freq_fondamentale = st.sidebar.slider(
    "Frequenza Fondamentale (Hz)", 
    min_value=50.0, 
    max_value=880.0, 
    value=220.0, 
    step=1.0
)

durata = st.sidebar.slider("Durata Audio (secondi)", 0.5, 3.0, 1.5)
sample_rate = 44100  # Frequenza di campionamento standard

# --- Main: Selezione Armonici ---
st.subheader("Selezione Armonici")
cols = st.columns(6)
attivi = []
nomi_armonici = [
    "Fondamentale",
    "2° (Ottava)",
    "3° (Quinta)",
    "4° (2 Ottave)",
    "5° (3ª Magg.)",
    "6° (Quinta)"
]

# Volumi decrescenti per un suono più naturale (come nella realtà)
volumi_base = [0.5, 0.4, 0.3, 0.2, 0.15, 0.1]

for i in range(6):
    with cols[i]:
        is_attivo = st.checkbox(f"{i+1}°", value=(i == 0), key=f"h{i}")
        attivi.append(is_attivo)
        st.caption(nomi_armonici[i])
        st.write(f"{freq_fondamentale * (i+1):.1f} Hz")

# --- Sintesi Sonora ---
t = np.linspace(0, durata, int(sample_rate * durata), endpoint=False)
onda_risultante = np.zeros_like(t)

for i, attivo in enumerate(attivi):
    if attivo:
        frequenza = freq_fondamentale * (i + 1)
        ampiezza = volumi_base[i]
        onda_risultante += ampiezza * np.sin(2 * np.pi * frequenza * t)

# Normalizzazione per evitare clipping (distorsione)
if np.max(np.abs(onda_risultante)) > 0:
    onda_risultante = onda_risultante / np.max(np.abs(onda_risultante))

# --- Visualizzazione ---
st.subheader("Visualizzazione Forma d'Onda")

# Mostriamo solo un piccolo segmento (es. 20ms) per vedere i cicli dell'onda
segmento_mostrato = int(0.02 * sample_rate) 
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=t[:segmento_mostrato], 
    y=onda_risultante[:segmento_mostrato],
    line=dict(color='#38bdf8', width=2),
    name="Onda Risultante"
))

fig.update_layout(
    template="plotly_dark",
    height=300,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="Tempo (s)",
    yaxis_title="Ampiezza",
    yaxis=dict(range=[-1.1, 1.1])
)
st.plotly_chart(fig, use_container_width=True)

# --- Audio Player ---
st.subheader("Ascolta il Suono")
st.audio(onda_risultante, sample_rate=sample_rate)

# --- Footer Informativo ---
st.divider()
c1, c2 = st.columns(2)
with c1:
    st.info("""
    **Cos'è la serie armonica?**
    In fisica, ogni suono complesso è composto da una somma di onde sinusoidali. 
    La frequenza più bassa è la **fondamentale**, mentre le altre sono multipli interi.
    """)
with c2:
    st.success("""
    **Perché cambia il suono?**
    Aggiungendo armonici, la forma d'onda diventa meno "liscia" e più complessa. 
    Questo processo è chiamato **Sintesi Additiva**.
    """)