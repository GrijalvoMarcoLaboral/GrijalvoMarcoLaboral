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
                    # Agregamos fila con estilo específico para manejar el overflow
                    noticias_filas += f"<tr><td>{titulo_es}</td><td><a href=\"{entry.link}\">Leer aquí</a></td></tr>\n"
        except Exception as e:
            print(f"Error procesando {url}: {e}")
    
    if not noticias_encontradas:
        noticias_filas = "<tr><td colspan='2'>No hay noticias nuevas esta semana</td></tr>\n"

    # BLOQUE HTML MEJORADO
    # Se añade 'table-layout: fixed' y anchos definidos para evitar desbordamiento
    nuevo_bloque = f'''<!-- NOTICIAS_START -->
<div style="height: 300px; overflow-y: scroll; border: 1px solid #30363d; padding: 10px; border-radius: 6px; background-color: #0d1117; font-size: 14px;">
<table style="width: 100%; border-collapse: collapse; table-layout: fixed;">
  <thead>
    <tr style="background-color: #21262d; color: #c9d1d9;">
      <th style="padding: 8px; text-align: left; width: 70%;">📰 Noticia</th>
      <th style="padding: 8px; text-align: left; width: 30%;">🔗 Enlace</th>
    </tr>
  </thead>
  <tbody>
    {noticias_filas}
  </tbody>
</table>
</div>
<!-- NOTICIAS_END -->'''

    if os.path.exists(ARCHIVO_MD):
        with open(ARCHIVO_MD, "r", encoding="utf-8") as f:
            contenido = f.read()

        if "<!-- NOTICIAS_START -->" in contenido:
            # Reemplaza el bloque existente usando DOTALL para cubrir múltiples líneas
            nuevo_contenido = re.sub(r"<!-- NOTICIAS_START -->.*?<!-- NOTICIAS_END -->", nuevo_bloque, contenido, flags=re.DOTALL)
        else:
            # Si no está, lo añade al final
            nuevo_contenido = contenido + "\n\n" + nuevo_bloque
            
        with open(ARCHIVO_MD, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)
        print("¡README actualizado con scroll fijo!")

if __name__ == "__main__":
    obtener_noticias()
