import feedparser
import re
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator
import os

ARCHIVO_MD = "README.md"
URLS = ["https://thehackernews.com/feeds/posts/default", "https://feeds.feedburner.com/SecurityWeek"]

def obtener_bloque_noticias(fecha_inicio, fecha_fin):
    """
    Genera el bloque HTML/Markdown para un periodo específico.
    Si no hay noticias, devuelve un bloque indicando que no hubo actividad.
    """
    # Formateo del período (Ej: "2026/05/21 al 2026/05/28")
    fecha_inicio_str = fecha_inicio.strftime('%Y/%m/%d')
    fecha_fin_str = fecha_fin.strftime('%Y/%m/%d')
    periodo_str = f"{fecha_inicio_str} al {fecha_fin_str}"

    # Iniciamos el string de noticias vacío
    noticias_items = ""
    noticias_encontradas = False

    for url in URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Verificamos que tenga fecha de publicación
                if not hasattr(entry, 'published_parsed'):
                    continue
                
                fecha_pub = datetime(*entry.published_parsed[:6])

                # Filtramos por rango de fechas
                if fecha_inicio <= fecha_pub <= fecha_fin:
                    noticias_encontradas = True
                    try:
                        titulo_es = GoogleTranslator(source='auto', target='es').translate(entry.title)
                    except Exception:
                        # Si falla la traducción, dejamos el título original
                        titulo_es = entry.title
                    
                    fecha_pub_str = fecha_pub.strftime('%Y/%m/%d')

                    # DISEÑO DE BURBUJA (MANTENIDO IGUAL)
                    # MODIFICACIÓN: Se usa HTML <a> con target="_blank" para abrir en nueva pestaña
                    bloque_noticia = f"""
> 📅 **{fecha_pub_str}**
> ### {titulo_es}
> 
> <b><a href="{entry.link}" target="_blank">🔗 Ir al enlace ↗</a></b>

---
"""
                    noticias_items += bloque_noticia

        except Exception as e:
            print(f"Error procesando {url}: {e}")

    # Estructura Markdown nativa con <details> (MANTENIDA IGUAL)
    if noticias_encontradas:
        markdown_final = f'''
<details>
<summary><b>📦 Ver Noticias Recientes ({periodo_str})</b></summary>
<br/>

{noticias_items}

</details>'''
    else:
        # Si no hay noticias esa semana, creamos un bloque vacío para mantener la estructura de 5
        markdown_final = f'''
<details>
<summary><b>📦 Ver Noticias Recientes ({periodo_str})</b></summary>
<br/>

_No se encontraron noticias en este período._

</details>'''
        
    return markdown_final

def main():
    hoy = datetime.now()
    
    # 1. Generar el bloque de la SEMANA ACTUAL (Los últimos 7 días)
    inicio_semana_actual = hoy - timedelta(days=7)
    bloque_actual = obtener_bloque_noticias(inicio_semana_actual, hoy)
    
    # 2. Leer el archivo actual para recuperar bloques antiguos
    if os.path.exists(ARCHIVO_MD):
        with open(ARCHIVO_MD, "r", encoding="utf-8") as f:
            contenido = f.read()
    else:
        contenido = ""

    # 3. Extraer los bloques <details> existentes que estén dentro de nuestros comentarios
    lista_bloques_existentes = []
    
    # Buscamos el contenido entre los marcadores
    match = re.search(r"<!-- NOTICIAS_START -->(.*?)<!-- NOTICIAS_END -->", contenido, flags=re.DOTALL)
    if match:
        # Extraemos todos los bloques <details> individualmente
        lista_bloques_existentes = re.findall(r"<details>[\s\S]*?</details>", match.group(1))

    # 4. Lógica Cíclica de 5 Semanas
    # Mantenemos los primeros 4 bloques existentes (las semanas inmediatamente anteriores)
    bloques_a_mantener = lista_bloques_existentes[:4]
    
    # Construimos la nueva lista: Nueva semana + 4 anteriores
    nuevos_bloques = [bloque_actual] + bloques_a_mantener
    
    # 5. Relleno automático (Backfill)
    # Si por alguna razón tenemos menos de 5 bloques (ej. primer ejecución),
    # buscamos en weeks más antiguas para completar las 5 casillas visuales.
    semanas_necesarias = 5 - len(nuevos_bloques)
    if semanas_necesarias > 0:
        # Empezamos a buscar desde 2 semanas atrás hasta 5 semanas atrás
        for i in range(2, 2 + semanas_necesarias):
            fin_busqueda = hoy - timedelta(days=(7 * (i - 1)))
            inicio_busqueda = hoy - timedelta(days=(7 * i))
            
            bloque_historico = obtener_bloque_noticias(inicio_busqueda, fin_busqueda)
            nuevos_bloques.append(bloque_historico)

    # Unimos todos los bloques con saltos de línea
    contenido_markdown_final = "\n".join(nuevos_bloques)
    
    # 6. Guardar cambios en el README.md
    # Reemplazamos todo lo que esté entre los comentarios
    if "<!-- NOTICIAS_START -->" in contenido:
        nuevo_contenido = re.sub(
            r"<!-- NOTICIAS_START -->.*?<!-- NOTICIAS_END -->", 
            f"<!-- NOTICIAS_START -->\n{contenido_markdown_final}\n<!-- NOTICIAS_END -->", 
            contenido, 
            flags=re.DOTALL
        )
    else:
        # Si no existen los comentarios, los agregamos al final
        nuevo_contenido = contenido + f"\n<!-- NOTICIAS_START -->\n{contenido_markdown_final}\n<!-- NOTICIAS_END -->"
    
    with open(ARCHIVO_MD, "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)
    
    print("README.md actualizado con los últimos 5 periodos semanales.")

if __name__ == "__main__":
    main()
