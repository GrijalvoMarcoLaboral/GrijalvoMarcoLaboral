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
    noticias_encontradas = False

    for url in URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                fecha_pub = datetime(*entry.published_parsed[:6])
                if fecha_pub > inicio_periodo:
                    noticias_encontradas = True
                    titulo_es = GoogleTranslator(source='auto', target='es').translate(entry.title)
                    noticias_filas += f"| {titulo_es} | [Leer aquí]({entry.link}) |\n"
        except Exception as e:
            print(f"Error procesando {url}: {e}")
    
    if not noticias_encontradas:
        noticias_filas = "| No hay noticias nuevas esta semana | N/A |\n"

    # Este es el bloque con estilo para el scroll
    # Usamos un div con una altura fija y scroll activado
    nuevo_bloque = (
        "<!-- NOTICIAS_START -->\n"
        '<div style="height: 300px; overflow-y: scroll; border: 1px solid #444; padding: 10px;">\n\n'
        "| 📰 Noticia | 🔗 Enlace |\n| :--- | :--- |\n"
        f"{noticias_filas}"
        "\n</div>\n"
        "<!-- NOTICIAS_END -->"
    )

    if os.path.exists(ARCHIVO_MD):
        with open(ARCHIVO_MD, "r", encoding="utf-8") as f:
            contenido = f.read()

        if "<!-- NOTICIAS_START -->" in contenido:
            # Reemplaza el bloque existente
            nuevo_contenido = re.sub(r"<!-- NOTICIAS_START -->.*?<!-- NOTICIAS_END -->", nuevo_bloque, contenido, flags=re.DOTALL)
        else:
            # Si no está, lo añade después del título de noticias
            nuevo_contenido = contenido + "\n\n" + nuevo_bloque
            
        with open(ARCHIVO_MD, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)
        print("¡README actualizado con scroll!")

if __name__ == "__main__":
    obtener_noticias()
