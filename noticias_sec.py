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

    # Iniciamos el string de noticias vacío
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

                    # DISEÑO DE BURBUJA (BLOQUE DE CITA)
                    # Usamos '>' para crear el recuadro.
                    # Usamos '###' para el título H3.
                    # El enlace va al final.
                    bloque_noticia = f"""
> 📅 **{fecha_pub_str}**
> ### {titulo_es}
> 
> **[🔗 Ir al enlace ↗]({entry.link})**

---
"""
                    noticias_items += bloque_noticia

        except Exception as e:
            print(f"Error procesando {url}: {e}")

    if noticias_encontradas:
        # Estructura Markdown nativa
        # Usamos <details> que es compatible con GitHub MD para colapsar
        markdown_final = f'''
<details>
<summary><b>📦 Ver Noticias Recientes ({periodo_str})</b></summary>
<br/>

{noticias_items}

</details>
'''
        return markdown_final
    else:
        return "_No se encontraron noticias esta semana._"

# Función principal para guardar en el archivo
if __name__ == "__main__":
    contenido_markdown = obtener_noticias()
    
    # Leemos el archivo actual
    if os.path.exists(ARCHIVO_MD):
        with open(ARCHIVO_MD, "r", encoding="utf-8") as f:
            contenido = f.read()

        # Reemplazamos el bloque de noticias si existe, o lo agregamos al final
        if "<!-- NOTICIAS_START -->" in contenido:
            nuevo_contenido = re.sub(r"<!-- NOTICIAS_START -->.*?<!-- NOTICIAS_END -->", f"<!-- NOTICIAS_START -->\n{contenido_markdown}\n<!-- NOTICIAS_END -->", contenido, flags=re.DOTALL)
        else:
            nuevo_contenido = contenido + f"\n<!-- NOTICIAS_START -->\n{contenido_markdown}\n<!-- NOTICIAS_END -->"
        
        # Guardamos cambios
        with open(ARCHIVO_MD, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)
        
        print("¡README.md actualizado con formato Markdown puro!")
