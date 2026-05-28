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
    
    # Formateamos el rango de fechas para el encabezado
    fecha_inicio_str = inicio_periodo.strftime('%Y/%m/%d')
    fecha_fin_str = hoy.strftime('%Y/%m/%d')
    periodo_str = f"{fecha_inicio_str} al {fecha_fin_str}"

    noticias_items = ""
    noticias_encontradas = False

    for url in URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                fecha_pub = datetime(*entry.published_parsed[:6])
                
                # Solo noticias de la última semana
                if fecha_pub > inicio_periodo:
                    noticias_encontradas = True
                    titulo_es = GoogleTranslator(source='auto', target='es').translate(entry.title)
                    
                    # Formateamos la fecha de la noticia individual (YYYY/MM/DD)
                    fecha_pub_str = fecha_pub.strftime('%Y/%m/%d')
                    
                    # Generamos el item HTML con la fecha antes del título
                    noticias_items += f'''
<div class="news-item" style="margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #21262d;">
  <!-- Fecha de la noticia individual -->
  <span style="display: inline-block; background: rgba(56, 139, 253, 0.15); color: #58a6ff; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; font-family: monospace; margin-bottom: 4px;">{fecha_pub_str}</span>
  
  <!-- Título -->
  <div style="font-weight: 600; color: #c9d1d9; margin-bottom: 4px;">{titulo_es}</div>
  
  <!-- Enlace -->
  <a href="{entry.link}" style="color: #58a6ff; text-decoration: none; font-size: 0.9rem;">Leer noticia completa →</a>
</div>'''
        except Exception as e:
            print(f"Error procesando {url}: {e}")
    
    if not noticias_encontradas:
        noticias_items = '<div style="color: #8b949e; padding: 10px;">No hay noticias nuevas este periodo.</div>'

    # BLOQUE HTML CON BOTÓN DESPLEGABLE (DETAILS)
    # Esto es 100% compatible con GitHub y no necesita scroll complejo
    nuevo_bloque = f'''<!-- NOTICIAS_START -->

<details>
  <!-- Texto del botón -->
  <summary style="background-color: #21262d; padding: 12px 16px; cursor: pointer; font-weight: 600; color: #58a6ff; border-radius: 6px; user-select: none;">Desplegar Noticias 📰</summary>
  
  <!-- Contenido que se abre al hacer clic -->
  <div style="padding: 16px; background-color: #0d1117; border: 1px solid #30363d; border-top: none; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px; margin-top: 6px;">
    
    <!-- Indicador del periodo -->
    <div style="margin-bottom: 15px; color: #8b949e; font-size: 0.9rem; font-style: italic; border-bottom: 1px solid #30363d; padding-bottom: 8px;">
      📅 Periodo obtenido: {periodo_str}
    </div>

    {noticias_items}
    
  </div>
</details>

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
        print("¡README actualizado con botón desplegable y fechas!")

if __name__ == "__main__":
    obtener_noticias()
