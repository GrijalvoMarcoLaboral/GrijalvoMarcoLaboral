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
        print("No hay noticias nuevas.")
        return

    if os.path.exists(ARCHIVO_MD):
        with open(ARCHIVO_MD, "r", encoding="utf-8") as f:
            contenido = f.read()

        # El nuevo bloque HTML con diseño oscuro y scroll
        nuevo_bloque_html = (
            "\n"
            '<div style="height: 350px; overflow-y: auto; border: 1px solid #30363d; padding: 20px; '
            'border-radius: 12px; background-color: #0d1117; color: #c9d1d9; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">' 
            '\n\n'
            "| 📰 Noticia | 🔗 Enlace |\n| :--- | :--- |\n"
            f"{noticias_filas}"
            "\n</div>\n"
            ""
        )

        patron = r".*?"
        
        if re.search(patron, contenido, re.DOTALL):
            nuevo_contenido = re.sub(patron, nuevo_bloque_html, contenido, flags=re.DOTALL)
            with open(ARCHIVO_MD, "w", encoding="utf-8") as f:
                f.write(nuevo_contenido)
            print("¡README actualizado con éxito!")
        else:
            print("Error: No se encontraron los marcadores y en tu README.")

if __name__ == "__main__":
    obtener_noticias()
