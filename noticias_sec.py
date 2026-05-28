import feedparser
import re
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator
import os

ARCHIVO_MD = "README.md"
URLS = ["https://thehackernews.com/feeds/posts/default", "https://feeds.feedburner.com/SecurityWeek"]

def obtener_noticias():
    hoy = datetime.now()
    inicio_periodo = hoy - timedelta(days=7)
    noticias_filas = ""

    for url in URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                fecha_pub = datetime(*entry.published_parsed[:6])
                if fecha_pub > inicio_periodo:
                    titulo_es = GoogleTranslator(source='auto', target='es').translate(entry.title)
                    noticias_filas += f"| {titulo_es} | [Leer aquí]({entry.link}) |\n"
        except Exception as e:
            print(f"Error procesando {url}: {e}")
    
    if os.path.exists(ARCHIVO_MD):
        with open(ARCHIVO_MD, "r", encoding="utf-8") as f:
            contenido = f.read()

        nuevo_bloque = (
            "<!-- NOTICIAS_START -->\n"
            '<div style="height: 350px; overflow-y: auto; border: 1px solid #30363d; padding: 20px; '
            'border-radius: 12px; background-color: #0d1117; color: #c9d1d9; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">'
            '\n\n| 📰 Noticia | 🔗 Enlace |\n| :--- | :--- |\n'
            f"{noticias_filas}"
            "\n</div>\n"
            "<!-- NOTICIAS_END -->"
        )

        # Reemplaza todo lo que esté entre las etiquetas o crea el bloque si no existe
        if "<!-- NOTICIAS_START -->" in contenido:
            nuevo_contenido = re.sub(r"<!-- NOTICIAS_START -->.*?<!-- NOTICIAS_END -->", nuevo_bloque, contenido, flags=re.DOTALL)
        else:
            nuevo_contenido = contenido + "\n\n" + nuevo_bloque
            
        with open(ARCHIVO_MD, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)
        print("¡README actualizado con éxito!")

if __name__ == "__main__":
    obtener_noticias()
