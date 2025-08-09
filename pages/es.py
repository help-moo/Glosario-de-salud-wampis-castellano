import streamlit as st
import pandas as pd
from pathlib import Path

######### CONFIG #########
st.set_page_config(initial_sidebar_state="collapsed")

@st.cache_data
def get_first_letter(word):
    word = word.lstrip("¿").strip()  # Elimina "¿" y espacios iniciales
    return word[0].upper() if word else ""

######### TÍTULO #########
st.markdown('## Glosario de salud wampis-castellano')

##################### Cargar CSV #####################
df = pd.read_csv("corpus_entries.csv", encoding="utf-8")

##################### Función para renderizar contenido de la entrada #####################
def render_entry(entry):
    # Audio si existe
    if pd.notna(entry["audio"]):
        audio_path = Path(entry["audio"])
        if audio_path.exists():
            st.audio(str(audio_path), format="audio/wav", autoplay=False)
        else:
            st.warning(f"Archivo de audio no encontrado: {audio_path}")

    # Información
    st.markdown(f"""
    <style>
    .label {{ font-weight: bold; font-size: 14px; margin-top: 6px; }}
    .value {{ font-size: 13px; margin-bottom: 6px; }}
    </style>
    <p class="label">Definición:</p><p class="value">{entry["mainheadword"]}</p>
    <p class="label">Parte del habla:</p><p class="value">{entry["partofspeech"]}</p>
    <p class="label">Dominio semántico:</p><p class="value">{entry["semanticdomain"]}</p>
    """, unsafe_allow_html=True)

##################### Definir el diálogo dinámico #####################
def show_dialog(entry):
    @st.dialog(entry["definitionorgloss"])  # Título del modal = palabra principal
    def _():
        render_entry(entry)
    _()

##################### BUSCADOR #####################
col1, col2 = st.columns([0.8, 0.2], vertical_alignment="bottom")

with col1:
    st.markdown("### Buscador")
    text_search = st.text_input("Buscar por palabra", value="").strip()

with col2:
    st.page_link('app.py', label="Wampis", use_container_width=True)
    st.page_link('pages/es.py', label="Castellano", disabled=True, use_container_width=True)

# Filtrado por búsqueda
df_filtered = df[df["definitionorgloss"].str.contains(text_search, case=False, na=False)].head(20) if text_search else None

##################### Mostrar resultados #####################
with st.container(border=True):
    if df_filtered is not None and not df_filtered.empty:
        st.write(f"Mostrando {len(df_filtered)} resultados:")
        for idx, entry in df_filtered.iterrows():
            if st.button(entry["definitionorgloss"], key=f"btn_search_{idx}", use_container_width=True):
                show_dialog(entry)

    elif text_search:
        st.info("No se encontraron resultados para la búsqueda.")

    else:
        # Obtener letras que tienen palabras
        letters_with_results = sorted(set(df["definitionorgloss"].dropna().apply(get_first_letter).str.upper()))

        if letters_with_results:
            for tab, letter in zip(st.tabs(letters_with_results), letters_with_results):
                with tab:
                    df_letter = df[df["definitionorgloss"].apply(get_first_letter).str.upper() == letter]
                    for idx, entry in df_letter.iterrows():
                        if st.button(entry["definitionorgloss"], key=f"btn_{letter}_{idx}", use_container_width=True):
                            show_dialog(entry)
        else:
            st.info("No hay palabras que empiecen con ninguna letra.")
