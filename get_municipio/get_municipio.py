import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

def cargar_datos_locales(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"El fichero '{file_path}' no fue encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"El fichero '{file_path}' no contiene un JSON válido.")
        return {}

@app.route('/<string:municipio>', methods=['GET'])
def get_municipio(municipio):
    path = os.path.join(os.path.dirname(__file__), "datosMunicipio.json")
    datos = cargar_datos_locales(path)   
    info_municipio = datos.get(municipio)
    
    if not info_municipio:
        return jsonify({"error": "Municipio no encontrado"}), 404
        
    respuesta_schema = {
        "fuente": "local",
        "datos_basicos": info_municipio
    }
    return jsonify(respuesta_schema)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)