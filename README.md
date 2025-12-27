# 📚 Fausti-Script  

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Este repositorio agrupa scripts para automatizar algunos procesos de la Universidad Nacional José Faustino Sánchez Carrión (UNJFSC). En particular, automatiza la **descarga de tesis** y el **análisis de asesores** del repositorio institucional.

## 🚀 Características  

- **Descarga de PDFs**  
  - Guarda las tesis con nombres de archivo limpios en la carpeta `tesis/`  
  - Elimina automáticamente caracteres inválidos en los nombres de archivo 

- **Extracción de asesores**  
  - Recolecta los nombres de los asesores de todas las tesis  
  - Normaliza los nombres (tildes, mayúsculas, espacios)  
  - Genera un ranking de los asesores más frecuentes  
  - Muestra los resultados en una tabla ordenada  

## 📋 Requisitos  

- Python 3.8 o superior  

## 🛠️ Instalación  

1. Clona el repositorio:
```bash
git clone [https://github.com/sudorios/fausti-script]
cd scrapy
```

2. Crea y activa un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
```env
BASE=https://repositorio.unjfsc.edu.pe
COLLECTION_PATH=/handle/UNJFSC/7
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
```

## ▶️ Uso  

1. Asegúrate de tener configurado el archivo `.env`  
2. Ejecuta el script principal:
```bash
python app.py
```

El script realizará lo siguiente:
1. Obtendrá la lista de tesis del repositorio  
2. Descargará los PDFs en la carpeta `tesis/`  
3. Analizará y normalizará los nombres de los asesores  
4. Mostrará un ranking de los asesores más frecuentes  

## 📂 Estructura del proyecto  

```
scrapy/
├── tesis/               # Carpeta donde se guardan las tesis descargadas
├── .env                 # Archivo de configuración (crear manualmente)
├── app.py               # Script principal
├── requirements.txt     # Dependencias de Python
└── README.md           # Este archivo
```

## 📊 Ejemplo de salida  

```
=== Ranking de Asesores ===
1. Pérez Gómez, Juan (15 tesis)
2. Rodríguez López, María (12 tesis)
3. García Hernández, Carlos (8 tesis)
...
```

## ⚠️ Notas importantes  

- El script incluye pausas entre solicitudes para no sobrecargar el servidor  
- Los nombres de los asesores se normalizan automáticamente  
- Se recomienda ejecutar el script en horarios de menor tráfico    

## 🤝 Contribuciones  

Las contribuciones son bienvenidas. Por favor, envía un Pull Request con tus mejoras.  

## 📧 Contacto  

Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio.  

---

## 📦 Requirements  

Install the dependencies:  

```bash
pip install requests beautifulsoup4 matplotlib

