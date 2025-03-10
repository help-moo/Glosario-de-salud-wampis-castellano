from pydub import AudioSegment
import os

BASE_PATH = "App/AudioVisual/"
OUTPUT_PATH = "App/audiovisual2/"
AUDIO_FORMAT_LIST = ["wav"]  # Formatos de audio que quieres procesar

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

# Obtener lista de archivos en el directorio
_, _, filenames = next(os.walk(BASE_PATH), (None, None, []))

# Procesar cada archivo de audio
for filename in filenames:
    for audio_format in AUDIO_FORMAT_LIST:
        if filename.endswith("." + audio_format):
            file_path = os.path.join(BASE_PATH, filename)  # Ruta completa del archivo original
            output_path = os.path.join(OUTPUT_PATH, filename)  # Ruta donde se guardará el archivo modificado
            
            # Cargar archivo de audio
            sound = AudioSegment.from_file(file_path, format=audio_format)
            
            # Normalizar audio
            normalized_sound = match_target_amplitude(sound, -14.0)
            
            # Asegurar que la carpeta de salida existe
            os.makedirs(OUTPUT_PATH, exist_ok=True)
            
            # Exportar archivo normalizado
            normalized_sound.export(output_path, format=audio_format)
            print(f"Archivo procesado y guardado: {output_path}")
