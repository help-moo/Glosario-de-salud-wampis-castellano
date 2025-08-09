import streamlit as st
import pandas as pd
from pathlib import Path
import unicodedata


######### CONFIG #########
st.set_page_config(initial_sidebar_state="collapsed")

######### TITULO #########
st.title("Glosario de salud wampis-castellano")
    
##################### Cargar CSV #####################
df = pd.read_csv("corpus_entries.csv", encoding="utf-8")

##################### Estado para entrada seleccionada #####################
if "selected_entry" not in st.session_state:
    st.session_state.selected_entry = None

##################### Función para quitar tildes #####################
def remove_accents(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(input_str))
        if unicodedata.category(c) != 'Mn'
    )

##################### BUSCADOR y FILTRADO #####################
col1, col2 = st.columns([0.8, 0.2], vertical_alignment="bottom")

with col1:
    text_search = st.text_input("Buscar por palabra", value="").strip()

with col2:
    st.page_link('wampis-castellano.py', label="Wampis", use_container_width=True, disabled=True)
    st.page_link('pages/1-castellano-wampis.py', label="Castellano", use_container_width=True)

# Filtrado por búsqueda
df_filtered = df[df["mainheadword"].str.contains(text_search, case=False, na=False)].head(20) if text_search else None

##################### Función para mostrar entrada #####################

##################### inyectar CSS para modificar .dialog ######################
st.markdown("""
<style>
.st-bp.st-em.st-en.st-eo.st-c1.st-ep.st-ef.st-eq.st-er {
    padding: 1.5rem 1.5rem 0rem !important;
}

.st-emotion-cache-2vdko {
    display: block !important;
}
</style>
""", unsafe_allow_html=True)

######################### St.dialog para mostrar entrada #########################

@st.cache_data
def render_entry(entry):
    if pd.notna(entry["audio"]):
        audio_path = Path(entry["audio"])
        if audio_path.exists():
            st.audio(str(audio_path), format="audio/wav", autoplay=False)
        else:
            st.warning(f"Archivo de audio no encontrado: {audio_path}")

    st.markdown(f"""
    <div style="font-size:16px; font-weight:bold;">Definición:</div>
    <div style="font-size:18px; margin-top:0; margin-bottom:8px;">{entry["definitionorgloss"]}</div>

    <div style="font-size:16px; font-weight:bold; margin-bottom:4px;">Clase de palabra:</div>
    <div style="font-size:18px; margin-top:0; margin-bottom:8px;">{entry["partofspeech"]}</div>

    <div style="font-size:16px; font-weight:bold; margin-bottom:4px;">Dominio semántico:</div>
    <div style="font-size:18px; margin-top:0; margin-bottom:18px;">{entry["semanticdomain"]}</div>
    """, unsafe_allow_html=True)


##################### Definir el diálogo #####################
def show_dialog(entry):
    @st.dialog(entry["mainheadword"])  # Usar la palabra como título
    def _():
        render_entry(entry)
    _()

##################### Mostrar resultados #####################
with st.container(border=True):
    if df_filtered is not None and not df_filtered.empty:
        st.write(f"Mostrando {len(df_filtered)} resultados:")
        for _, entry in df_filtered.iterrows():
            label = f'**{entry["mainheadword"]}**'
            if pd.notna(entry["audio"]) and entry["audio"].strip() != "":
                label += " 🔊"
            label += f' - {entry["definitionorgloss"]}'
            if st.button(label, key=entry["mainheadword"], use_container_width=True):
                st.session_state.selected_entry = entry
                show_dialog(entry)
    elif text_search:
        st.info("No se encontraron resultados para la búsqueda.")
    else:
        # Agrupar letras sin acentos
        first_letters = (
            df["mainheadword"]
            .dropna()
            .apply(lambda w: remove_accents(w.strip())[0].upper() if w.strip() else "")
        )
        letters_with_results = sorted(set(first_letters))

        if letters_with_results:
            for tab, letter in zip(st.tabs(letters_with_results), letters_with_results):
                with tab:
                    df_letter = df[
                        df["mainheadword"].apply(
                            lambda w: remove_accents(w.strip()).upper().startswith(letter)
                        )
                    ]
                    for _, entry in df_letter.iterrows():
                        label = f'**{entry["mainheadword"]}**'
                        if pd.notna(entry["audio"]) and entry["audio"].strip() != "":
                            label += " 🔊"
                        label += f' - {entry["definitionorgloss"]}'
                        if st.button(label, key=f"{letter}-{entry['mainheadword']}", use_container_width=True):
                            st.session_state.selected_entry = entry
                            show_dialog(entry)
        else:
            st.info("No hay palabras que empiecen con ninguna letra.")
            
st.markdown("""
<div style="text-align:center; margin-top:10px; font-size:14px; color:#444;">
  <p style="font-size:12px; color:#888;">© 2025 GELCOP</p>  
  <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank" style="display:inline-block;">
    <img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc-nd.png" alt="Licencia CC BY-NC-ND 4.0" height="30" />
  </a>
</div>
""", unsafe_allow_html=True)



# ##################### BUSCADOR wampis #####################

# text_search = st.text_input("Buscar por palabra clave o definición", value="").strip()

# # Filtrado (solo si hay búsqueda)
# df_search = pd.DataFrame()  # Inicializa DataFrame vacío
# if text_search:
#     mask1 = df["mainheadword"].fillna("").str.contains(text_search, case=False, na=False)
#     #mask2 = df["definitionorgloss"].fillna("").str.contains(text_search, case=False, na=False)
#     df_search = df[mask1].head(20)  # Mostrar solo los 20 primeros resultados 
#     #df_search = df[mask1 | mask2].head(20)  # Mostrar solo los 20 primeros resultados
# # else:

# #     df_search = df  # Si no hay búsqueda, mostramos todo

# if not df_search.empty:
#     st.write(f"Mostrando {len(df_search)} resultados:")
#     with st.container():
#         for _, entry in df_search.iterrows():
#             with st.expander(entry["mainheadword"]):
#                 html_str = f"""
#                 <style>
#                 .label {{
#                     font-weight: bold;
#                     font-size: 14px;
#                     margin-top: 6px;
#                 }}
#                 .value {{
#                     font-size: 13px;
#                     margin-bottom: 6px;
#                 }}
#                 </style>
#                 <p class="label">Definición:</p>
#                 <p class="value">{entry["definitionorgloss"]}</p>
#                 <p class="label">Parte del habla:</p>
#                 <p class="value">{entry["partofspeech"]}</p>
#                 <p class="label">Dominio semántico:</p>
#                 <p class="value">{entry["semanticdomain"]}</p>
#                 """
#                 st.markdown(html_str, unsafe_allow_html=True)
# else:
#   if text_search:  # Solo mostrar advertencia si hubo búsqueda
#       st.warning("No se encontraron resultados.")

# ##################### FILTRADO EN TABLAS - ALFABETICO #####################

# # Crear pestañas por cada letra del abecedario
# letters = list(string.ascii_uppercase)
# tabs = st.tabs(letters)

# # Iterar sobre cada pestaña y filtrar el DataFrame
# for tab, letter in zip(tabs, letters):
#     with tab:
#         # Filtrar palabras que empiezan con la letra correspondiente
#         df_filtered = df[df["mainheadword"].str.upper().str.startswith(letter)]
        
#         # Mostrar resultados si hay coincidencias
#         if not df_filtered.empty:
#             st.write(f"**Palabras que empiezan con '{letter}':**")
#             for _, entry in df_filtered.iterrows():
#                 with st.expander(entry["mainheadword"]):
#                     html_str = f"""
#                     <style>
#                     .label {{ font-weight: bold; color: #2C3E50; font-size: 14px; margin-top: 6px; }}
#                     .value {{ font-size: 13px; color: #333; margin-bottom: 6px; }}
#                     </style>
#                     <p class="label">Definición:</p>
#                     <p class="value">{entry["definitionorgloss"]}</p>
#                     <p class="label">Parte del habla:</p>
#                     <p class="value">{entry["partofspeech"]}</p>
#                     <p class="label">Dominio semántico:</p>
#                     <p class="value">{entry["semanticdomain"]}</p>
#                     """
#                     st.markdown(html_str, unsafe_allow_html=True)
#         else:
#             st.info(f"No hay palabras que empiecen con '{letter}'.")
































#st.write(df)

# for index, entry in df.iterrows():
#     html_str = f"""
#     <style>
#     .entry-container {{
#         border: 2px solid #4A90E2;
#         border-radius: 8px;
#         padding: 12px;
#         margin: 12px 0;
#         background-color: #f9f9f9;
#         box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
#     }}
#     .mainheadword {{
#         font-size: 22px;
#         font-weight: bold;
#         color: #E74C3C;
#         margin-bottom: 8px;
#         border-bottom: 1px solid #ddd;
#         padding-bottom: 4px;
#     }}
#     .label {{
#         font-weight: bold;
#         color: #2C3E50;
#         font-size: 14px;
#         margin-top: 6px;
#     }}
#     .value {{
#         font-size: 13px;
#         color: #333;
#         margin-bottom: 6px;
#     }}
#     </style>

#     <div class="entry-container">
#         <p class="mainheadword">{entry["mainheadword"]}</p>
#         <p class="label">Definición:</p>
#         <p class="value">{entry["definitionorgloss"]}</p>
#         <p class="label">Parte del habla:</p>
#         <p class="value">{entry["partofspeech"]}</p>
#         <p class="label">Dominio semántico:</p>
#         <p class="value">{entry["semanticdomain"]}</p>
#     </div>
#     """

#     st.markdown(html_str, unsafe_allow_html=True)

# import streamlit as st

# for index, entry in df.iterrows():
#     with st.expander(entry["mainheadword"]):
#         html_str = f"""
#         <style>
#         .label {{
#             font-weight: bold;
#             color: #2C3E50;
#             font-size: 14px;
#             margin-top: 6px;
#         }}
#         .value {{
#             font-size: 13px;
#             color: #333;
#             margin-bottom: 6px;
#         }}
#         </style>
#         <p class="label">Definición:</p>
#         <p class="value">{entry["definitionorgloss"]}</p>
#         <p class="label">Parte del habla:</p>
#         <p class="value">{entry["partofspeech"]}</p>
#         <p class="label">Dominio semántico:</p>
#         <p class="value">{entry["semanticdomain"]}</p>
#         """
#         st.markdown(html_str, unsafe_allow_html=True)

###### PRUEBA CON AUDIO#######
# for index, entry in df.iterrows():
#     with st.expander(entry["mainheadword"]):
#         st.markdown(
        #     f"""
        #     <style>
        #     .label {{ font-weight: bold; color: #2C3E50; font-size: 14px; margin-top: 6px; }}
        #     .value {{ font-size: 13px; color: #333; margin-bottom: 6px; }}
        #     </style>
        #     <p class="label">Definición:</p><p class="value">{entry["definitionorgloss"]}</p>
        #     <p class="label">Parte del habla:</p><p class="value">{entry["partofspeech"]}</p>
        #     <p class="label">Dominio semántico:</p><p class="value">{entry["semanticdomain"]}</p>
        #     """,
        #     unsafe_allow_html=True
        # )

        # # Mostrar audio si la ruta es válida
        # if pd.notna(entry["audio"]):  
        #     audio_path = Path(entry["audio"])
        #     if audio_path.exists():
        #         st.audio(str(audio_path), format="audio/wav", autoplay=False)
        #     else:
        #         st.warning(f"Archivo de audio no encontrado: {audio_path}")

##################### FILTRADO EN TABLAS - CLASE DE PALABRA #####################

# # Obtener las categorías únicas de "partofspeech"
# parts_of_speech = df["partofspeech"].unique().tolist()

# # Crear pestañas dinámicamente
# tabs = st.tabs(parts_of_speech)

# # Iterar sobre cada pestaña y filtrar el DataFrame
# for tab, pos in zip(tabs, parts_of_speech):
#     with tab:
#         df_filtered = df[df["partofspeech"] == pos]

#         # Mostrar resultados si hay coincidencias
#         if not df_filtered.empty:
#             st.write(f"**Palabras en la categoría '{pos}':**")
#             for _, entry in df_filtered.iterrows():
#                 with st.expander(entry["mainheadword"]):
#                     html_str = f"""
#                     <style>
#                     .label {{ font-weight: bold; color: #2C3E50; font-size: 14px; margin-top: 6px; }}
#                     .value {{ font-size: 13px; color: #333; margin-bottom: 6px; }}
#                     </style>
#                     <p class="label">Definición:</p>
#                     <p class="value">{entry["definitionorgloss"]}</p>
#                     <p class="label">Dominio semántico:</p>
#                     <p class="value">{entry["semanticdomain"]}</p>
#                     """
#                     st.markdown(html_str, unsafe_allow_html=True)
#         else:
#             st.info(f"No hay palabras en la categoría '{pos}'.")

