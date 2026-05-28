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
                    # Generamos fila HTML con estilos inline para compatibilidad GitHub
                    noticias_filas += f"<tr><td style='padding: 8px; border-bottom: 1px solid #21262d; color: #8b949e; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{titulo_es}</td><td style='padding: 8px; border-bottom: 1px solid #21262d;'><a href='{entry.link}'>Leer</a></td></tr>\n"
        except Exception as e:
            print(f"Error procesando {url}: {e}")
    
    if not noticias_encontradas:
        noticias_filas = "<tr><td colspan='2' style='padding: 10px; color: #8b949e;'>No hay noticias nuevas esta semana</td></tr>\n"

    # BLOQUE HTML MEJORADO (CSS INLINE PARA GITHUB)
    # 1. max-height: Obliga a tener un límite.
    # 2. overflow-y: scroll: Habilita la barra vertical.
    # 3. overflow-x: hidden: Evita que la tabla rompa el ancho.
    # 4. table-layout: fixed: Fuerza a la tabla a respetar las dimensiones.
    nuevo_bloque = f'''<!-- NOTICIAS_START -->
<div style="max-height: 300px; overflow-y: scroll; overflow-x: hidden; border: 1px solid #30363d; padding: 10px; border-radius: 6px; background-color: #0d1117;">
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
            nuevo_contenido = re.sub(r"<!-- NOTICIAS_START -->.*?<!-- NOTICIAS_END -->", nuevo_bloque, contenido, flags=re.DOTALL)
        else:
            nuevo_contenido = contenido + "\n\n" + nuevo_bloque
            
        with open(ARCHIVO_MD, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)
        print("¡README actualizado con scroll optimizado!")

if __name__ == "__main__":
    obtener_noticias()
