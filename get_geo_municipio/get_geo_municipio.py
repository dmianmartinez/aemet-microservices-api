import requests
import os
from flask import Flask, jsonify

app = Flask(__name__)

BASE_URL_AEMET = "https://opendata.aemet.es/opendata/api"

@app.route('/<string:municipio>/geo', methods=['GET'])
def get_geo_municipio(municipio):
        
    headers = {'api_key': os.getenv("AEMET_API_KEY")}
    url = f"{BASE_URL_AEMET}/maestro/municipios"
    
    try:
        response = requests.get(url, headers=headers)
        response_data = requests.get(response.json()['datos'], headers=headers)
        for registro in response_data.json():
            
            if registro["url"].startswith(municipio):                
                respuesta_schema = {
                    "municipioid": registro.get('id'),
                    "latitud": registro.get('latitud_dec'),
                    "longitud": registro.get('longitud_dec'),
                    "altitud": registro.get('altitud'),
                }
                return jsonify({
                    "fuente": "AEMET OpenData",
                    "datos_geograficos": respuesta_schema
                })
        return jsonify({"error": "Datos geográficos no encontrados"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al obtener datos de AEMET: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)