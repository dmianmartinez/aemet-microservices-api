import json
from flask import Flask, jsonify
import requests

app = Flask(__name__)
    
SERVICE_URLS = {
    "geo": "http://getgeomunicipio:5000/",
    "meteo": "http://getmeteomunicipio:5000/",
    "demo": "http://getdemomunicipio:5000/"
}

@app.route('/<string:municipio>/<string:tipo1>/<string:tipo2>/', methods=['GET'])
def getVariosMunicipio(municipio, tipo1, tipo2):

    resultado_final = {}
    tipos = {tipo1, tipo2}
    
    for tipo in tipos:
        try:
            url = f"{SERVICE_URLS[tipo]}/{municipio}/{tipo}"
            
            response = requests.get(url)
            
            datos_servicio = response.json()
            
            resultado_final.update(datos_servicio)

        except requests.exceptions.RequestException as e:
            print(f"Error llamando al servicio '{tipo}': {e}")

    if not resultado_final:
         return jsonify({"error": "Ninguno de los servicios solicitados pudo ser procesado."}), 503

    return jsonify(resultado_final)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)