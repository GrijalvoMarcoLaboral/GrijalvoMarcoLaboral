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
                    
                    # DISEÑO DE TARJETA (CARD)
                    # Usamos display flex para alinear texto y botón
                    noticias_items += f'''
<div style="background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; gap: 10px; transition: border-color 0.2s;">
  
  <div style="flex: 1;">
    <span style="font-size: 0.75rem; color: #8b949e; display: block; margin-bottom: 4px;">📅 {fecha_pub_str}</span>
    <!-- Título en NEGRITA y color principal -->
    <div style="font-weight: bold; color: #c9d1d9; font-size: 0.95rem; line-height: 1.4;">{titulo_es}</div>
  </div>

  <!-- Botón de acción (Ir al enlace) -->
  <a href="{entry.link}" target="_blank" style="background-color: #238636; color: #ffffff; text-decoration: none; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; white-space: nowrap; display: inline-block;">Ir al enlace</a>
  
</div>'''
        except Exception as e:
            print(f"Error procesando {url}: {e}")
    
    if not noticias_encontradas:
        noticias_items = '<div style="color: #8b949e; padding: 10px;">No hay noticias nuevas este periodo.</div>'

    # BLOQUE HTML FINAL
    # Nota: Se usan etiquetas < y > reales para renderizar HTML en GitHub
    nuevo_bloque = f'''<!-- NOTICIAS_START -->

<details>
  <summary style="background-color: #21262d; padding: 12px 16px; cursor: pointer; font-weight: 600; color: #58a6ff; border-radius: 6px; user-select: none;">Desplegar Noticias 📰</summary>
  
  <div style="padding: 16px; background-color: #161b22; border: 1px solid #30363d; border-top: none; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px; margin-top: 6px;">
    
    <div style="margin-bottom: 20px; color: #8b949e; font-size: 0.9rem; font-style: italic; border-bottom: 1px solid #30363d; padding-bottom: 8px;">
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
        print("¡README actualizado con diseño de tarjetas!")

if __name__ == "__main__":
    obtener_noticias()
