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

    # Formateo del período actual (Ej: "2026/05/21 al 2026/05/28")
    fecha_inicio_str = inicio_periodo.strftime('%Y/%m/%d')
    fecha_fin_str = hoy.strftime('%Y/%m/%d')
    periodo_str = f"{fecha_inicio_str} al {fecha_fin_str}"

    # Encabezado de la tabla en Markdown profesional
    noticias_items = "| Fecha | Período del Reporte | Título de la Noticia | Enlace |\n"
    noticias_items += "| :--- | :--- | :--- | :---: |\n"
    
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

                    # Agregamos la fila a la tabla con formato Markdown nativo
                    # El enlace se renderiza como un botón de texto plano estilizado por GitHub
                    noticias_items += f"| 📅 {fecha_pub_str} | `{periodo_str}` | **{titulo_es}** | [Ir al enlace ↗]({entry.link}) |\n"

        except Exception as e:
            print(f"Error procesando {url}: {e}")

    if noticias_encontradas:
        # Envolvemos la tabla Markdown dentro del desplegable nativo de GitHub
        markdown_final = f'''
<details>
<summary><b>📦 Ver Noticias Recientes ({periodo_str})</b></summary>

{noticias_items}
</details>
'''
        return markdown_final
    else:
        return "_No se encontraron noticias esta semana._"
