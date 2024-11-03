import os
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    file_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.get("/entries")
async def get_entries():
    try:
        # Ruta al archivo JSON
        file_path = os.path.join(os.path.dirname(__file__), "base/edu.json")
        print(f"Leyendo archivo desde: {file_path}")  # Verificar la ruta

        # Carga el archivo JSON
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            print("Archivo JSON cargado:", data)  # Verificar el contenido completo del JSON

        # Extraer el campo "entries" y verificarlo
        entries = data.get("entries", [])
        print("Contenido de 'entries':", entries)  # Verificar el contenido de entries

        # Devuelve la lista de entries
        return {"entries": entries}
    except Exception as e:
        print("Error al leer el archivo JSON:", str(e))  # Imprimir el error en caso de excepción
        return {"error": str(e)}
