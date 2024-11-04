from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

# Ruta para obtener las entradas desde el archivo JSON
@app.get("/entries")
async def get_entries():
    try:
        # Ajusta la ruta para encontrar edu.json en la carpeta base
        file_path = os.path.join(os.path.dirname(__file__), "edu.json")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Devuelve las entradas, o una lista vacía si no existen
            return {"entries": data.get("entries", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar los datos: {e}")

# Ruta para procesar las respuestas del usuario
@app.post("/chat")
async def process_chat(user_responses: dict):
    try:
        # Carga las entradas desde el archivo JSON
        file_path = os.path.join(os.path.dirname(__file__), "edu.json")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            entries = data.get("entries", [])

        confirmed_intelligences = []
        no_response_index = 0  # Contador para el número de respuestas "no"

        # Procesar las respuestas del usuario
        for entry in entries:
            name = entry.get("name")
            description = entry.get("description")
            props = entry.get("props", [])
            no_responses = entry.get("no_responses", [])

            # Verificar las respuestas del usuario
            for prop in props:
                if prop in user_responses:
                    response = user_responses[prop].lower()
                    if response == "sí":
                        confirmed_intelligences.append({"name": name, "description": description})
                        break  # Confirmamos esta inteligencia y pasamos a la siguiente
                    elif response == "no":
                        # Si la respuesta es "no", incrementamos el índice de respuestas "no"
                        if no_response_index < len(no_responses):
                            recommendation = no_responses[no_response_index]
                            no_response_index += 1
                            return {"recommendation": recommendation}
        
        # Retornar las inteligencias confirmadas
        return {"confirmed_intelligences": confirmed_intelligences}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar las respuestas: {e}")
