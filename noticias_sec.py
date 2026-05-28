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
                
                if fecha_pub > inicio_periodo:
                    noticias_encontradas = True
                    titulo_es = GoogleTranslator(source='auto', target='es').translate(entry.title)
                    fecha_pub_str = fecha_pub.strftime('%Y/%m/%d')
                    
                    # DISEÑO RESPONSIVE FINAL
                    # - flex-wrap: permite que el botón baje si la pantalla es chica
                    # - text-overflow: ellipsis corta el texto largo si no cabe
                    noticias_items += f'''
<div style="background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 12px; margin-bottom: 12px; display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
  
  <!-- Zona de Texto (Ocupa todo el espacio disponible pero respeta límites) -->
  <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center;">
    <span style="font-size: 0.75rem; color: #8b949e; margin-bottom: 4px;">📅 {fecha_pub_str}</span>
    
    <!-- Título con recorte automático si es muy largo -->
    <div style="font-weight: bold; color: #c9d1d9; font-size: 0.95rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{titulo_es}">{titulo_es}</div>
  </div>

  <!-- Botón (No se aplasta, mantiene su forma) -->
  <a href="{entry.link}" target="_blank" style="background-color: #238636; color: #ffffff; text-decoration: none; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; white-space: nowrap; flex-shrink: 0;">Ir al enlace</a>
  
</div>'''
        except Exception as e:
            print(f"Error procesando {url}: {e}")
    
    if not noticias_encontradas:
        noticias
