import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

# Índice global para las respuestas "NO"
response_index = {}

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    file_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.get("/entries")
async def get_entries():
    try:
        # Ruta al archivo JSON
        file_path = os.path.join(os.path.dirname(__file__), "edu.json")
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
        raise HTTPException(status_code=500, detail="Error al cargar los datos.")

@app.post("/chat")
async def chat(user_responses: dict):
    global response_index  # Utiliza la variable global

    try:
        # Ruta al archivo JSON
        file_path = os.path.join(os.path.dirname(__file__), "edu.json")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        confirmed_intelligences = []
        no_responses = []

        # Procesar las respuestas del usuario
        for entry in data['entries']:
            name = entry['name']
            props = entry['props']

            # Revisar si el usuario ha respondido 'sí' a alguna de las propiedades
            for prop in props:
                if user_responses.get(prop) == "sí":
                    confirmed_intelligences.append({
                        "name": name,
                        "description": entry["description"]
                    })
                    response_index[name] = 0  # Inicializar el índice para esta inteligencia
                    break  # Salir del bucle si se confirma la inteligencia

        # Procesar respuestas "NO"
        for entry in confirmed_intelligences:
            name = entry["name"]
            if name in response_index:
                index = response_index[name]
                if index < len(data['entries'][data['entries'].index(entry)]['no_responses']):
                    no_response = data['entries'][data['entries'].index(entry)]['no_responses'][index]
                    no_responses.append(no_response)
                    response_index[name] += 1  # Incrementar el índice para la próxima respuesta

        # Si hay respuestas "NO", reiniciar el proceso
        if no_responses:
            response_index = {}  # Reiniciar el índice global para comenzar de cero
            return {
                "no_responses": no_responses,
                "message": "Reiniciando el proceso. Por favor, responde a las preguntas nuevamente."
            }

        # Retornar las inteligencias confirmadas y las respuestas "NO"
        return {
            "confirmed_intelligences": confirmed_intelligences,
            "no_responses": no_responses
        }

    except Exception as e:
        print("Error en la conversación:", str(e))
        raise HTTPException(status_code=500, detail="Error en el procesamiento de la conversación.")
