import json
from flask import Flask, jsonify
import requests
import os


app = Flask(__name__)

def cargar_datos_locales(fichero):
    try:
        with open(fichero, 'r', encoding='utf-8') as f:
            print(f)
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"No se ha podido leer el json"}
    
BASE_URL_AEMET = "https://opendata.aemet.es/opendata/api"

@app.route('/<string:municipio>/demo', methods=['GET'])
def get_demo_municipio(municipio):
    path = os.path.join(os.path.dirname(__file__), "datosMunicipio.json")
    datos = cargar_datos_locales(path)    
    
    info_municipio = datos.get(municipio)
    
    if not info_municipio:
        return jsonify({"error": "Municipio no encontrado"}), 404
    
    headers = {'api_key': os.getenv("AEMET_API_KEY")}    
    municipio_id = "id"+str(info_municipio.get("municipioid"))
    url = f"{BASE_URL_AEMET}/maestro/municipio/{municipio_id}"
    numhabitantes = 0
    try:
        response = requests.get(url, headers=headers)
        response_data = requests.get(response.json()['datos'], headers=headers).json()[0]
        num_habitantes = response_data.get("num_hab")

    except:
         return jsonify({"error": "Error al obtener datos de AEMET"}), 500
        
    respuesta_schema = {
        "municipioid": info_municipio.get("municipioid"),
        "alcalde": info_municipio.get("alcalde"),
        "partidopolitico": info_municipio.get("partidopolitico"),
        "numhabitantes": num_habitantes
    }
    return jsonify({
        "fuente": "local / API AEMET OpenData",
        "datos_demograficos": respuesta_schema
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)