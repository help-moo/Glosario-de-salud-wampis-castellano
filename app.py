import streamlit as st
import pandas as pd
from corpus import df
from pathlib import Path

######### CONFIG #########
st.set_page_config(
    initial_sidebar_state="collapsed")

######### TITULO #########
st.markdown('## Glosario de salud wampis-castellano')

##################### BUSCADOR y FILTRADO #####################

col1, col2 = st.columns([0.8, 0.2],vertical_alignment = "bottom")

with col1:
    st.markdown("### Buscador")
    text_search = st.text_input("Buscar por palabra", value="").strip()

with col2:
    st.page_link('app.py', label= "Wampis", use_container_width = True, disabled=True)
    st.page_link('pages/es.py',label = "Castellano", use_container_width = True)
    

# Filtrado por búsqueda
df_filtered = df[df["mainheadword"].str.contains(text_search, case=False, na=False)].head(20) if text_search else None

# Función para mostrar entrada
def render_entry(entry):
    # Mostrar audio si la ruta es válida
    if pd.notna(entry["audio"]):  
        audio_path = Path(entry["audio"])
        if audio_path.exists():
            st.audio(str(audio_path), format="audio/wav", autoplay=False)
        else:
            st.warning(f"Archivo de audio no encontrado: {audio_path}")

    # Mostrar información de la entrada
    st.markdown(f"""
    <style>
    .label {{ font-weight: bold; font-size: 14px; margin-top: 6px; }}
    .value {{ font-size: 13px; margin-bottom: 6px; }}
    </style>
    <p class="label">Definición:</p><p class="value">{entry["definitionorgloss"]}</p>
    <p class="label">Parte del habla:</p><p class="value">{entry["partofspeech"]}</p>
    <p class="label">Dominio semántico:</p><p class="value">{entry["semanticdomain"]}</p>
    """, unsafe_allow_html=True)

# Mostrar resultados de búsqueda o pestañas alfabéticas
with st.container(border=True):
    if df_filtered is not None and not df_filtered.empty:
        st.write(f"Mostrando {len(df_filtered)} resultados:")
        for _, entry in df_filtered.iterrows():
            with st.expander(entry["mainheadword"]):
                render_entry(entry)
    elif text_search:
        st.info("No se encontraron resultados para la búsqueda.")
    else:
        letters_with_results = sorted(set(df["mainheadword"].dropna().str[0].str.upper()))

        if letters_with_results:
            for tab, letter in zip(st.tabs(letters_with_results), letters_with_results):
                with tab:
                    df_letter = df[df["mainheadword"].str.upper().str.startswith(letter)]
                    for _, entry in df_letter.iterrows():
                        with st.expander(entry["mainheadword"]):
                            render_entry(entry)
        else:
            st.info("No hay palabras que empiecen con ninguna letra.")


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

