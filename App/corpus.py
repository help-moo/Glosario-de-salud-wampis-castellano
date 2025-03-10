from bs4 import BeautifulSoup
import pandas as pd
import re

class Entry:
    def __init__(self, mainheadword, mainheadword_lang, definitionorgloss, definitionorgloss_lang, partofspeech, semanticdomain, audio):
        self.mainheadword = mainheadword
        self.mainheadword_lang = mainheadword_lang
        self.definitionorgloss = definitionorgloss
        self.definitionorgloss_lang = definitionorgloss_lang
        self.partofspeech = partofspeech
        self.semanticdomain = semanticdomain
        self.audio = audio
    
    def __repr__(self):
        return f"{self.mainheadword}"

# Ruta del archivo XHTML
file_path = "corpus.xhtml"

# Cargar el archivo
with open(file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extraer las entradas con class="entry"
entries = []

for entry in soup.find_all(class_="entry"):
    mainheadword_elem = entry.find(class_="mainheadword")
    definition_elem = entry.find(class_="definitionorgloss")
    partofspeech_elem = entry.find(class_="partofspeech")
    semanticdomain_elem = entry.find(class_="semanticdomain")
    audio_elem = entry.find("audio")
    
    # Extraer texto asegurando que se capture todo el contenido
    headword_text = mainheadword_elem.get_text(" ", strip=True) if mainheadword_elem else None
    gloss_text = definition_elem.get_text(" ", strip=True) if definition_elem else None
    partofspeech_text = partofspeech_elem.get_text(" ", strip=True) if partofspeech_elem else None
    semanticdomain_text = semanticdomain_elem.get_text(" ", strip=True) if semanticdomain_elem else None
    audio_src = audio_elem.find("source")["src"] if audio_elem and audio_elem.find("source") else None
    
    # Extraer atributos de idioma
    headword_lang = mainheadword_elem.find("span")["lang"] if mainheadword_elem and mainheadword_elem.find("span") else None
    gloss_lang = definition_elem.find("span")["lang"] if definition_elem and definition_elem.find("span") else None
    
    # Aplicar limpieza y transformación de texto
    def limpiar_headword(texto):
        if pd.isna(texto):  
            return texto
        texto = texto.replace("\n", " ")  # Reemplazar saltos de línea con espacio
        texto = re.sub(r"^[a-z]\.", "", texto)  # Eliminar "x. " al inicio
        return texto.strip()  # Eliminar espacios extra

    def capitalizar(texto):
        if isinstance(texto, str) and texto.startswith("¿"):
            for i, c in enumerate(texto):
                if c.isalpha():  # Encuentra la primera letra después del "¿"
                    return texto[:i] + c.upper() + texto[i+1:]
        return texto.capitalize()

    def trim_espacios(texto):
        if isinstance(texto, str):  
            return re.sub(r'\s+', ' ', texto.strip())  # Reemplaza múltiples espacios por un solo espacio
        return texto

    # Aplicar correcciones a los valores extraídos
    headword_text = limpiar_headword(headword_text)
    gloss_text = trim_espacios(gloss_text)
    gloss_text = capitalizar(gloss_text)

    # Corregir la ruta del audio usando regex
    if audio_src:
        audio_src = re.sub(r".*[\\/]", "", audio_src)  # Tomar solo el nombre del archivo
        audio_src = f"AudioVisual/{audio_src}"  # Unir con "AudioVisual/"
    
    entries.append(Entry(headword_text, headword_lang, gloss_text, gloss_lang, partofspeech_text, semanticdomain_text, audio_src))

# Convertir las entradas en un DataFrame
df = pd.DataFrame([e.__dict__ for e in entries])
print(df)
