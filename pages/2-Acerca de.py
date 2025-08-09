import streamlit as st

######### CONFIG #########
st.set_page_config(page_title="Acerca de", initial_sidebar_state="expanded")

######### TÍTULO Y TEXTO #########
st.markdown("""
## Acerca de esta aplicación

Esta es una versión web de un glosario bilingüe wampis-castellano y castellano-wampis para atención en salud. El glosario está dividido en un léxico básico y una serie de frases comunes utilizadas por personal de salud para obtener información que permita ayudar a sus pacientes.

Diseñado y elaborado por miembros del Grupo para el Estudio de Lenguas y Culturas Originarias Peruanas de la Pontificia Universidad Católica del Perú, con el apoyo del Vicerrectorado de Investigación a través del proyecto PI0734, y de la Facultad de Letras y Ciencias Humanas.

**Asesoría en wampis y grabaciones:** Dina Socorro Ananco Ahuananchi  

**Diseño, análisis e implementación:** Josué Nuñez Guerrero, Rosa Luisa Gonzales Mendoza  

**Coordinación del proyecto:** Jaime Peña Torrejón  
            
**Repositorio GitHub:** [https://github.com/GELCOP/Glosario-de-salud-wampis-castellano](https://github.com/GELCOP/Glosario-de-salud-wampis-castellano)

**Contacto:** [grupo.estudiolenguas@pucp.edu.pe](mailto:grupo.estudiolenguas@pucp.edu.pe)

<div align="center">
  <img src="https://github.com/user-attachments/assets/afcda9f3-32bd-4694-84aa-3007cafc5247" alt="GELCOP" width="350" />
</div>

---

<div align="center">
  <p>Este trabajo se encuentra disponible bajo la siguiente licencia:</p>
  <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank">
    <img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc-nd.png" alt="Licencia CC BY-NC-ND 4.0" height="30" />
  </a>
</div>
""", unsafe_allow_html=True)
