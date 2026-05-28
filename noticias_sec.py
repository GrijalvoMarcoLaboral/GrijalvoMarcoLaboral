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
    noticias_items = ""
    noticias_encontradas = False

    for url in URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                fecha_pub = datetime(*entry.published_parsed[:6])
                if fecha_pub > inicio_periodo:
                    noticias_encontradas = True
                    titulo_es = GoogleTranslator(source='auto', target='es').translate(entry.title)
                    
                    # Usamos <li> (lista) en vez de <tr> (tabla)
                    noticias_items += f'''
<li style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #21262d;">
  <div style="color: #c9d1d9; font-weight: 600; margin-bottom: 4px; display: block;">{titulo_es}</div>
  <a href="{entry.link}" style="color: #58a6ff; text-decoration: none; font-size: 0.9rem;">Leer noticia completa →</a>
</li>'''
        except Exception as e:
            print(f"Error procesando {url}: {e}")
    
    if not noticias_encontradas:
        noticias_items = '<li style="color: #8b949e;">No hay noticias nuevas esta semana.</li>'

    # NUEVO BLOQUE HTML CON LISTA (UL) Y SCROLL FIJO
    # Cambiamos Table por UL para asegurar que el scroll funcione en GitHub
    nuevo_bloque = f'''<!-- NOTICIAS_START -->

<!-- Título Opcional -->
<h3 style="border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-top: 24px;">📰 Noticias Ciberseguridad</h3>

<!-- Contenedor con Scroll Fijo -->
<div style="max-height: 300px; overflow-y: auto; overflow-x: hidden; border: 1px solid #30363d; padding: 12px; border-radius: 6px; background-color: #0d1117; font-size: 14px; scrollbar-width: thin;">
  
  <!-- Lista de Noticias (Reemplaza a la Tabla) -->
  <ul style="list-style: none; padding: 0; margin: 0;">
    {noticias_items}
  </ul>

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
        print("¡README actualizado con lista y scroll!")

if __name__ == "__main__":
    obtener_noticias()
