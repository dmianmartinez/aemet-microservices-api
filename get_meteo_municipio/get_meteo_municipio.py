import requests
import os
from datetime import datetime
from flask import Flask, jsonify


app = Flask(__name__)

BASE_URL_AEMET = "https://opendata.aemet.es/opendata/api"

@app.route('/<string:municipio>/meteo', methods=['GET'])
def get_meteo_municipio(municipio):
        
    headers = {'api_key': os.getenv("AEMET_API_KEY")}
    url = f"{BASE_URL_AEMET}/maestro/municipios"
    municipioid = None
    
    response = requests.get(url, headers=headers)
    response_data = requests.get(response.json()['datos'], headers=headers)
    for registro in response_data.json():
        if registro["url"].startswith(municipio):                
            municipio_id = registro.get('id').replace("id","")
            break
                
    if municipio_id is None:
        return jsonify({"error": "Datos geográficos no encontrados"}), 404

    try: 
        url = f"{BASE_URL_AEMET}/prediccion/especifica/municipio/horaria/{municipio_id}"
        url_diaria = f"{BASE_URL_AEMET}/prediccion/especifica/municipio/diaria/{municipio_id}"

        response = requests.get(url, headers=headers)
        response_data = requests.get(response.json()['datos'], headers=headers).json()[0]
        response_diaria = requests.get(url_diaria, headers=headers)
        response_data_diaria = requests.get(response_diaria.json()['datos'], headers=headers).json()[0]

        prediccion = response_data["prediccion"]["dia"][0]
        prediccion_diaria = response_data_diaria["prediccion"]["dia"][0]

        periodo = str(datetime.now().hour) if len(str(datetime.now().hour)) == 2 else "0" + str(datetime.now().hour)

        temperatura = {item['periodo']: item['value'] for item in prediccion["temperatura"]}
        temperatura_max = prediccion_diaria["temperatura"]["maxima"]
        temperatura_min = prediccion_diaria["temperatura"]["minima"]
        humedad = {item['periodo']: item['value'] for item in prediccion["humedadRelativa"]}
        precipitacion = {item['periodo']: item['value'] for item in prediccion["precipitacion"]}
        cielo = {item['periodo']: item['descripcion'] for item in prediccion["estadoCielo"]}
        viento = dict()
        for item in prediccion["vientoAndRachaMax"]:
            if 'direccion' in item and 'velocidad' in item:
                periodo = item['periodo']
        
                direccion = item['direccion'][0] if item['direccion'] else None
                velocidad = item['velocidad'][0] if item['velocidad'] else None
        
                viento[periodo] = {
                    'direccion': direccion,
                    'velocidad': velocidad
                }

        respuesta_schema = {
            "municipioid": municipioid,
            "temperatura_actual": temperatura.get(periodo),
            "temperaturas": [temperatura_max, temperatura_min],
            "humedad": humedad.get(periodo),
            "viento": viento.get(periodo),
            "precipitación": precipitacion.get(periodo),
            "estadocielo": cielo.get(periodo)
        }

        return jsonify({
            "fuente": "AEMET OpenData",
            "datos_meteorologicos": respuesta_schema
        })
    except:
        return jsonify({"error": "Datos meteorológicos no encontrados"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)