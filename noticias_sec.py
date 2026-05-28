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
    
    # Formato del periodo solicitado
    periodo_str = f"{inicio_periodo.strftime('%d/%m')} al {hoy.strftime('%d/%m/%Y')}"

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
                    fecha_pub_str = fecha_pub.strftime('%d/%m/%Y')
                    # Estructura de tabla profesional con enlace como botón de texto
                    noticias_filas += f"| {fecha_pub_str} | **{titulo_es}** | [🔗 Ir al enlace]({entry.link}) |\n"
        except Exception as e:
            print(f"Error procesando {url}: {e}")
    
    if not noticias_encontradas:
        noticias_filas = "| - | No hay noticias nuevas esta semana | - |"

    # Estructura del bloque final
    nuevo_bloque = (
        "\n"
        f"**Periodo de actualización:** `{periodo_str}`\n\n"
        "<details open>\n"
        "<summary><b>Haz clic para ver las noticias recientes</b></summary>\n\n"
        "| Fecha | Título de la noticia | Acción |\n"
        "| :--- | :--- | :---: |\n"
        f"{noticias_filas}"
        "\n</details>\n"
        ""
    )

    if os.path.exists(ARCHIVO_MD):
        with open(ARCHIVO_MD, "r", encoding="utf-8") as f:
            contenido = f.read()

        if "" in contenido:
            nuevo_contenido = re.sub(r".*?", nuevo_bloque, contenido, flags=re.DOTALL)
        else:
            nuevo_contenido = contenido + "\n\n" + nuevo_bloque
            
        with open(ARCHIVO_MD, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)
        print("¡README actualizado con éxito!")

if __name__ == "__main__":
    obtener_noticias()
