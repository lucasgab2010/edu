from fastapi import FastAPI
import json
import os

app = FastAPI()

@app.get("/entries")
async def get_entries():
    try:
        # Ajusta la ruta para encontrar edu.json en la carpeta base
        file_path = os.path.join(os.path.dirname(__file__), "edu.json")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return {"entries": data.get("entries", [])}  # Usa .get() para prevenir errores si entries falta
    except Exception as e:
        return {"error": f"Error al cargar los datos: {e}"}
