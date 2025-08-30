import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import time
from urllib.parse import urljoin
import re
from collections import Counter
import unicodedata
import difflib

load_dotenv()

BASE = os.getenv("BASE")
COLLECTION_PATH = os.getenv("COLLECTION_PATH")
COLLECTION_URL = BASE + COLLECTION_PATH

HEADERS = {
    "User-Agent": os.getenv("USER_AGENT")
}

def sanitize_filename(text):
    """Limpia el nombre de archivo para que sea válido en el sistema."""
    return re.sub(r'[\\/*?:"<>|]', "", text).replace(" ", "_")[:80]

def normalizar_nombre(nombre: str) -> str:
    """Normaliza el nombre (espacios, minúsculas, tildes)."""
    nombre = " ".join(nombre.split())
    nombre = nombre.lower()
    nombre = ''.join(
        c for c in unicodedata.normalize('NFD', nombre)
        if unicodedata.category(c) != 'Mn'
    )
    return nombre.title()

def normalizar_base(nombre: str) -> str:
    """Extrae solo los apellidos (parte antes de la coma)."""
    partes = nombre.split(",")
    return partes[0].strip() if len(partes) > 1 else nombre

def unificar_nombres(counter, umbral=0.75):
    """Unifica nombres similares o con la misma base de apellidos."""
    nombres = list(counter.keys())
    mapping = {}

    for nombre in nombres:
        base = normalizar_base(nombre)

        candidatos = [n for n in nombres if normalizar_base(n) == base]

        if len(candidatos) > 1:
            principal = max(candidatos, key=len)
            mapping[nombre] = principal
        else:
            similares = difflib.get_close_matches(nombre, nombres, n=1, cutoff=umbral)
            if similares:
                principal = max(similares, key=len)
                mapping[nombre] = principal
            else:
                mapping[nombre] = nombre

    nuevo_counter = Counter()
    for nombre, count in counter.items():
        nuevo_counter[mapping[nombre]] += count

    return nuevo_counter

def mostrar_tabla(counter):
    """Muestra ranking de asesores en tabla."""
    print("\n📊 Ranking de asesores más repetidos:\n")
    print(f"{'Asesor':50} | {'Cantidad'}")
    print("-" * 65)

    total = 0
    for asesor, count in counter.most_common():
        print(f"{asesor:50} | {count}")
        total += count

    print("-" * 65)
    print(f"{'TOTAL':50} | {total}")

def get_tesis_pages(offset=0):
    """Obtiene enlaces a páginas de tesis desde la colección."""
    url = COLLECTION_URL.format(offset=offset)
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.select(".artifact-title a")
    links = [urljoin(BASE, a["href"]) for a in items]

    return links

def descargar_pdf(thesis_page, out_folder="tesis"):
    """Descarga el PDF de una tesis en su carpeta destino."""
    r = requests.get(thesis_page, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    title_tag = soup.select_one("h2.page-header")
    title = title_tag.get_text(strip=True) if title_tag else "SIN_TITULO"

    thesis_id = thesis_page.split("/")[-1]

    pdf_link = soup.select_one("a[href*='/bitstream/handle/']")
    if not pdf_link:
        print(f"❌ No encontré PDF en {thesis_page}")
        return False

    pdf_url = urljoin(BASE, pdf_link["href"])

    safe_title = sanitize_filename(title)
    filename = f"{thesis_id}_{safe_title}.pdf"

    os.makedirs(out_folder, exist_ok=True)

    try:
        pdf_data = requests.get(pdf_url, headers=HEADERS)
        with open(os.path.join(out_folder, filename), "wb") as f:
            f.write(pdf_data.content)
        print(f"✅ Descargado: {filename}")
        return True
    except Exception as e:
        print(f"⚠️ Error descargando {pdf_url}: {e}")
        return False

def obtener_asesor(thesis_page):
    """Obtiene el asesor de la tesis (vista detallada)."""
    full_url = thesis_page + "?show=full"
    r = requests.get(full_url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("table tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            key = cols[0].get_text(strip=True)
            if "dc.contributor.advisor" in key.lower():
                return cols[1].get_text(strip=True)
    return "NO_ENCONTRADO"


def main():
    modo = input("Elige modo:\n1) Descargar PDFs\n2) Obtener asesores\n👉 ")

    offset = 0
    total = 0
    asesores_list = []

    while True:
        tesis_pages = get_tesis_pages(offset)
        if not tesis_pages:
            break

        print(f"📄 Página con offset {offset}, encontradas {len(tesis_pages)} tesis")

        for page in tesis_pages:
            if modo == "1":
                if descargar_pdf(page):
                    total += 1
            elif modo == "2":
                asesor = obtener_asesor(page)
                print(f"👨‍🏫 {page} → {asesor}")
                if asesor != "NO_ENCONTRADO":
                    asesores_list.append(normalizar_nombre(asesor))
                total += 1

            time.sleep(1)

        offset += 20  

    print(f"📂 Total procesados: {total}")

    if modo == "2" and asesores_list:
        counter = Counter(asesores_list)
        counter = unificar_nombres(counter)
        mostrar_tabla(counter)

if __name__ == "__main__":
    main()
